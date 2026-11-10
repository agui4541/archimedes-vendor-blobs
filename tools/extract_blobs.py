#!/usr/bin/env python3
"""Extract reviewed vendor files through elevated ADB or a local dump.

The manifest uses lines of the form:
  vendor:path[:destination]
Blank lines and comments are ignored. The tool refuses sensitive partitions.
"""
from __future__ import annotations
import argparse, hashlib, os, shlex, subprocess, sys
from pathlib import Path

SENSITIVE = ("nvram", "nvdata", "protect", "persist", "userdata", "metadata")
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "proprietary-files.txt"
OUT = ROOT / "proprietary"
META = ROOT / "metadata" / "extracted-files.tsv"

def parse_manifest():
    rows=[]
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if not line or line.startswith("#"): continue
        parts=line.split(":")
        if len(parts) not in (2,3): raise SystemExit(f"bad manifest line: {raw}")
        source, path = parts[:2]
        dest = parts[2] if len(parts)==3 else path
        low=path.lower()
        if any(token in low.split("/") for token in SENSITIVE):
            raise SystemExit(f"refusing sensitive path: {path}")
        rows.append((source,path,dest))
    return rows

def adb_pull(path: str, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Use adb pull so SELinux labels and permissions are not silently guessed.
    subprocess.run(["adb","pull",f"/{path}",str(dst)],check=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--adb",action="store_true",help="pull from the connected device")
    ap.add_argument("--source",type=Path,help="root of a local partition dump")
    args=ap.parse_args()
    if args.adb == bool(args.source):
        ap.error("choose exactly one of --adb or --source")
    rows=parse_manifest()
    records=[]
    for source,path,dest in rows:
        if source not in {"system","system_ext","product","vendor","odm","firmware"}:
            raise SystemExit(f"unsupported source partition: {source}")
        out=OUT / dest
        if args.adb:
            adb_pull(path,out)
        else:
            src=args.source / path
            if not src.is_file(): raise SystemExit(f"missing local source: {src}")
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_bytes(src.read_bytes())
        digest=hashlib.sha256(out.read_bytes()).hexdigest()
        records.append(f"{source}\t{path}\t{dest}\t{digest}\n")
    META.parent.mkdir(parents=True,exist_ok=True)
    META.write_text("source\toriginal_path\tdestination\tsha256\n"+"".join(records),encoding="utf-8")
    print(f"extracted {len(rows)} files")

if __name__ == "__main__": main()
