#!/usr/bin/env python3
"""Write the provenance and SHA-256 table for imported vendor files."""
from pathlib import Path
import hashlib
import struct

ROOT = Path(__file__).resolve().parents[1]
BUILD = "Xiaomi/full_Archimedes/Archimedes:9/PPR1.180610.011/462:userdebug/release-keys"
DATE = "2026-11-10"


def architecture(data: bytes) -> str:
    if data[:4] != b"\x7fELF" or len(data) < 20:
        return "data"
    elf_class = data[4]
    machine = struct.unpack_from("<H", data, 18)[0]
    if elf_class == 2 and machine == 183:
        return "64"
    if elf_class == 1 and machine == 40:
        return "32"
    return "unknown"


rows = []
for raw in (ROOT / "proprietary-files.txt").read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    source, path, *rest = line.split(":")
    dest = rest[0] if rest else path
    file_path = ROOT / "proprietary" / dest
    data = file_path.read_bytes()
    rows.append(
        "\t".join(
            (
                BUILD,
                source,
                path,
                dest,
                hashlib.sha256(data).hexdigest(),
                architecture(data),
                DATE,
                "read from elevated ADB; SELinux/dependencies require review",
            )
        )
    )

(ROOT / "metadata" / "extracted-files.tsv").write_text(
    "\t".join(
        (
            "build",
            "partition",
            "original_path",
            "destination",
            "sha256",
            "architecture",
            "extracted_at",
            "notes",
        )
    )
    + "\n"
    + "\n".join(rows)
    + "\n",
    encoding="utf-8",
)
print(f"wrote {len(rows)} metadata rows")
