#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tarfile
import tempfile
from pathlib import Path
from urllib.parse import urljoin

import requests
import zstandard as zstd

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = ("packagesite.txz", "packagesite.pkg", "packagesite.tzst", "repo.txz")
UA = "WebElbir-FreeBSD-Legacy-Pkg-Importer/1.0"


def jload(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def target_parts(target):
    m = re.fullmatch(r"FreeBSD:(\d+):(amd64|i386)", target)
    if not m:
        raise RuntimeError("bad target: " + target)
    return int(m.group(1)), m.group(2)


def abi_ok(target, *vals):
    major, arch = target_parts(target)
    s = " ".join(str(x) for x in vals if x).lower()
    if not s:
        return True
    m = re.search(r"freebsd[:\- ]+(\d+)", s)
    if m and int(m.group(1)) != major:
        return False
    if arch == "amd64":
        return "amd64" in s or "x86:64" in s or not any(x in s for x in ("i386", "x86:32"))
    return "i386" in s or "x86:32" in s or "*" in s


def normsum(v):
    if not isinstance(v, str):
        return None
    v = v.lower().strip().removeprefix("sha256:")
    return v if re.fullmatch(r"[0-9a-f]{64}", v) else None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def untar_member(blob, archive, names):
    bio = io.BytesIO(blob)
    if archive.endswith((".pkg", ".tzst")):
        with zstd.ZstdDecompressor().stream_reader(bio) as zr:
            bio = io.BytesIO(zr.read())
        mode = "r:"
    else:
        mode = "r:*"
    with tarfile.open(fileobj=bio, mode=mode) as tf:
        members = {Path(m.name).name: m for m in tf.getmembers() if m.isfile()}
        for name in names:
            if name in members:
                return name, tf.extractfile(members[name]).read()
    raise RuntimeError(f"{archive}: expected member not found")


def parse_yaml_lines(payload, source, target, priority, base=None, local=False):
    out = []
    for line in payload.decode("utf-8", "replace").splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        name, ver = str(r.get("name", "")), str(r.get("version", ""))
        if name and ver and abi_ok(target, r.get("abi"), r.get("arch")):
            out.append({"name": name, "version": ver, "r": r, "source": source,
                        "priority": priority, "base": base, "local": local})
    return out


def parse_old_sqlite(payload, source, target, priority, base):
    fd, tmp = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    con = None
    try:
        Path(tmp).write_bytes(payload)
        con = sqlite3.connect(tmp)
        con.row_factory = sqlite3.Row
        if not list(con.execute("PRAGMA table_info(packages)")):
            return []
        dcols = {x[1] for x in con.execute("PRAGMA table_info(deps)")}
        fk = next((x for x in ("package_id", "packageid", "pkg_id") if x in dcols), None)
        deps = {}
        if fk:
            for d in con.execute("SELECT * FROM deps"):
                d = dict(d)
                if d.get("name") and d.get(fk) is not None:
                    deps.setdefault(int(d[fk]), {})[str(d["name"])] = {
                        "origin": str(d.get("origin") or ""), "version": str(d.get("version") or "")}
        out = []
        for row in con.execute("SELECT * FROM packages"):
            d = dict(row)
            if not d.get("name") or not d.get("version") or not abi_ok(target, d.get("arch")):
                continue
            name, ver = str(d["name"]), str(d["version"])
            r = {"name": name, "origin": str(d.get("origin") or name), "version": ver,
                 "comment": str(d.get("comment") or ""), "desc": str(d.get("desc") or ""),
                 "arch": str(d.get("arch") or ""), "maintainer": str(d.get("maintainer") or "unknown"),
                 "www": str(d.get("www") or ""), "prefix": str(d.get("prefix") or "/usr/local"),
                 "flatsize": int(d.get("flatsize") or 0), "deps": deps.get(int(d.get("id") or 0), {}),
                 "path": f"All/{name}-{ver}.txz", "repopath": f"All/{name}-{ver}.txz"}
            for k in ("sum", "cksum", "checksum"):
                if normsum(d.get(k)):
                    r["sum"] = normsum(d[k])
                    break
            out.append({"name": name, "version": ver, "r": r, "source": source,
                        "priority": priority, "base": base, "local": False})
        return out
    finally:
        if con:
            con.close()
        Path(tmp).unlink(missing_ok=True)


def parse_catalog(blob, archive, source, target, priority, base=None, local=False):
    names = ("packagesite.yaml", "repo.sqlite") if archive == "repo.txz" else ("packagesite.yaml",)
    member, payload = untar_member(blob, archive, names)
    if member == "repo.sqlite":
        return parse_old_sqlite(payload, source, target, priority, base)
    return parse_yaml_lines(payload, source, target, priority, base, local)


def session():
    s = requests.Session()
    s.headers["User-Agent"] = UA
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
    return s


def remote_catalog(s, src, target, priority):
    errs = []
    for cat in CATALOGS:
        u = urljoin(src["url"], cat)
        try:
            r = s.get(u, timeout=(20, 180), allow_redirects=True)
            r.raise_for_status()
            rows = parse_catalog(r.content, cat, src["id"], target, priority, src["url"])
            if rows:
                print(target, src["id"], cat, len(rows))
                return rows
        except Exception as e:
            errs.append(f"{cat}:{type(e).__name__}")
    print(target, "WARN source failed", src["id"], ",".join(errs))
    return []


def relpath(c):
    r = c["r"]
    p = r.get("repopath") or r.get("path")
    if p:
        p = str(p).lstrip("/")
        return p if "/" in p else "All/" + p
    ext = ".txz" if target_parts(c["target"])[0] <= 11 else ".pkg"
    return f"All/{c['name']}-{c['version']}{ext}"


def local12(target, priority):
    oldall = ROOT / "All"
    if not oldall.is_dir():
        return []
    cat = next((ROOT / x for x in ("packagesite.pkg", "packagesite.txz") if (ROOT / x).exists()), None)
    if not cat:
        return []
    rows = parse_catalog(cat.read_bytes(), cat.name, "local-existing-12", target, priority, None, True)
    good = []
    for c in rows:
        c["target"] = target
        f = oldall / Path(relpath(c)).name
        if not f.exists():
            continue
        expected = normsum(c["r"].get("sum"))
        if expected and sha256(f) != expected:
            print(target, "WARN bad local checksum", f.name)
            continue
        c["local_file"] = str(f)
        good.append(c)
    print(target, "verified existing packages", len(good))
    return good


def is_root(name, cfg):
    if name in cfg.get("exact", []):
        return True
    f = cfg["families"]
    m = re.fullmatch(f["mysql"]["regex"], name)
    if m and int(m.group(1)) >= int(f["mysql"]["minimum_series"]):
        return True
    m = re.fullmatch(f["mariadb"]["regex"], name)
    if m and int(m.group(1)) >= int(f["mariadb"]["minimum_series"]):
        return True
    g = f["gcc"]
    return (g.get("include_generic") and name == g.get("generic_name", "gcc")) or bool(re.fullmatch(g["regex"], name))


def deps(c):
    d = c["r"].get("deps") or {}
    if isinstance(d, dict):
        return [(str(n), str(v.get("version")) if isinstance(v, dict) and v.get("version") else None) for n, v in d.items()]
    return []


def ordered(xs):
    return sorted(xs, key=lambda x: (x["priority"], x["source"], x["version"]))


def resolve(c, byname, selected, conflicts, stack):
    name = c["name"]
    if name in stack:
        return True
    if name in selected:
        if selected[name]["version"] != c["version"]:
            conflicts.append({"package": name, "selected": selected[name]["version"], "also_required": c["version"]})
        return True
    stack.add(name)
    for dn, dv in deps(c):
        opts = byname.get(dn, [])
        exact = [x for x in opts if not dv or x["version"] == dv]
        same = [x for x in exact if x["source"] == c["source"]]
        choices = ordered(same) + [x for x in ordered(exact) if x["source"] != c["source"]]
        if not choices and dv and opts:
            choices = ordered(opts)
            conflicts.append({"package": dn, "required_by": name, "required": dv,
                              "fallback": choices[0]["version"], "reason": "exact version unavailable"})
        if not choices or not resolve(choices[0], byname, selected, conflicts, stack):
            stack.remove(name)
            return False
    selected[name] = c
    stack.remove(name)
    return True


def select(rows, cfg):
    byname = {}
    for c in rows:
        byname.setdefault(c["name"], []).append(c)
    names = {n for n in byname if is_root(n, cfg)} | set(cfg.get("exact", []))
    g = cfg["families"]["gcc"]
    if g.get("include_generic"):
        names.add(g.get("generic_name", "gcc"))
    selected, conflicts, roots = {}, [], []
    for name in sorted(names):
        chosen = None
        attempts = []
        for c in ordered(byname.get(name, [])):
            trial = dict(selected)
            clen = len(conflicts)
            if resolve(c, byname, trial, conflicts, set()):
                selected, chosen = trial, c
                break
            del conflicts[clen:]
            attempts.append(c["source"] + ":" + c["version"])
        roots.append({"name": name, "status": "selected", "version": chosen["version"], "source": chosen["source"]}
                     if chosen else {"name": name, "status": "unresolved", "attempts": attempts})
    return selected, roots, conflicts


def urls(c):
    if not c.get("base"):
        return []
    p = relpath(c)
    fn = Path(p).name
    out = [urljoin(c["base"], p), urljoin(c["base"], "All/" + fn), urljoin(c["base"], fn)]
    return list(dict.fromkeys(out))


def materialize(s, c, out):
    fn = Path(relpath(c)).name
    dst = out / fn
    expected = normsum(c["r"].get("sum"))
    if dst.exists():
        got = sha256(dst)
        if not expected or got == expected:
            return dst, got
        dst.unlink()
    if c.get("local_file"):
        src = Path(c["local_file"])
        got = sha256(src)
        if not expected or got == expected:
            shutil.copy2(src, dst)
            return dst, got
    errs = []
    for u in urls(c):
        try:
            r = s.get(u, stream=True, timeout=(20, 300), allow_redirects=True)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            tmp = dst.with_suffix(dst.suffix + ".part")
            h = hashlib.sha256()
            with open(tmp, "wb") as f:
                for b in r.iter_content(1024 * 1024):
                    if b:
                        f.write(b); h.update(b)
            got = h.hexdigest()
            if expected and got != expected:
                tmp.unlink(missing_ok=True); errs.append("checksum:" + u); continue
            tmp.replace(dst)
            return dst, got
        except Exception as e:
            errs.append(type(e).__name__ + ":" + u)
    raise RuntimeError(f"cannot fetch {c['name']}-{c['version']} ({c['source']}): " + " | ".join(errs))


def txz(path, member, data):
    with tarfile.open(path, "w:xz") as tf:
        i = tarfile.TarInfo(member); i.size = len(data); i.mode = 0o644; i.mtime = 0
        tf.addfile(i, io.BytesIO(data))


def metadata(repo, selected, info):
    lines = []
    for name in sorted(selected):
        r = {k:v for k,v in selected[name]["r"].items() if not str(k).startswith("_")}
        r["path"] = r["repopath"] = "All/" + info[name]["filename"]
        r["sum"] = info[name]["sha256"]
        r["pkgsize"] = info[name]["size"]
        lines.append(json.dumps(r, separators=(",", ":"), ensure_ascii=False))
    data = ("\n".join(lines) + "\n").encode()
    txz(repo / "packagesite.txz", "packagesite.yaml", data)
    meta = ('version = 2;\npacking_format = "txz";\nmanifests = "packagesite.yaml";\n'
            'data = "data";\nfilesite = "filesite.yaml";\nmanifests_archive = "packagesite";\n'
            'filesite_archive = "filesite";\n').encode()
    (repo / "meta.conf").write_bytes(meta); (repo / "meta").write_bytes(meta)
    txz(repo / "meta.txz", "meta", meta)


def clean_old12():
    for d in ("All", "Libs"):
        p = ROOT / d
        if p.exists(): shutil.rmtree(p)
    for f in ("packagesite.pkg","packagesite.txz","data.pkg","data.txz","meta","meta.conf","meta.pkg","meta.txz",
              "digests.txz","SNAPSHOT_INFO.txt","SHA256SUMS","ROOTS_REQUESTED.txt"):
        (ROOT / f).unlink(missing_ok=True)


def build(target, migrate):
    cfg = jload(ROOT / "config/roots.json")
    sources = jload(ROOT / "config/sources.json")["targets"][target]
    man = ROOT / "MANIFESTS"; srcdir = ROOT / "SOURCES"; man.mkdir(exist_ok=True); srcdir.mkdir(exist_ok=True)
    if not sources:
        (man / (target.replace(":","-") + ".json")).write_text(json.dumps({"target":target,"status":"no-verified-source"},indent=2)+"\n")
        print(target, "no verified source; no fake URL used")
        return
    s = session(); rows = []; stats = []
    for pri, src in enumerate(sources):
        got = local12(target, pri) if src.get("type") == "local-existing" else remote_catalog(s, src, target, pri)
        for c in got: c["target"] = target
        rows += got; stats.append({"id":src["id"],"url":src.get("url"),"records":len(got)})
    if not rows: raise RuntimeError(target + ": no readable catalogues")
    selected, roots, conflicts = select(rows, cfg)
    if not selected: raise RuntimeError(target + ": no requested packages resolved")
    repo = ROOT / target / "latest"; out = repo / "All"; out.mkdir(parents=True, exist_ok=True); (repo / "Latest").mkdir(exist_ok=True)
    info = {}; errors = []
    for i, name in enumerate(sorted(selected), 1):
        c = selected[name]
        try:
            p, h = materialize(s, c, out)
            info[name] = {"filename":p.name,"sha256":h,"size":p.stat().st_size,"version":c["version"],
                          "source":c["source"],"role":"root" if is_root(name,cfg) else "dependency"}
            print(target, f"{i}/{len(selected)}", name, c["version"], "<-", c["source"])
        except Exception as e:
            errors.append({"name":name,"version":c["version"],"source":c["source"],"error":str(e)})
    if errors:
        (man / (target.replace(":","-") + ".failed.json")).write_text(json.dumps({"target":target,"errors":errors,"roots":roots,"conflicts":conflicts},indent=2)+"\n")
        raise RuntimeError(f"{target}: {len(errors)} package downloads failed")
    keep = {x["filename"] for x in info.values()}
    for p in out.iterdir():
        if p.is_file() and p.name not in keep and p.suffix in (".pkg",".txz",".tbz",".tgz"): p.unlink()
    metadata(repo, selected, info)
    (repo / "SHA256SUMS").write_text("".join(f"{x['sha256']}  All/{x['filename']}\n" for _,x in sorted(info.items())))
    report = {"target":target,"status":"ok","root_count":sum(x["role"]=="root" for x in info.values()),
              "package_count":len(info),"roots":roots,"packages":info,"dependency_version_conflicts":conflicts}
    (man / (target.replace(":","-") + ".json")).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    (srcdir / (target.replace(":","-") + ".json")).write_text(json.dumps({"target":target,"sources":stats},indent=2)+"\n")
    if migrate and target == "FreeBSD:12:amd64": clean_old12()
    print(target, "DONE", len(info), "packages")


def main():
    a = argparse.ArgumentParser(); a.add_argument("--target", required=True); a.add_argument("--migrate-existing-12", action="store_true")
    ns = a.parse_args()
    try:
        build(ns.target, ns.migrate_existing_12)
    except Exception as e:
        print("ERROR", e, file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
