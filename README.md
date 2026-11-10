# Archimedes vendor blobs

Proprietary vendor files for the Xiaomi Archimedes MT6761 device.

This repository is intentionally organized like a LineageOS device vendor repository. It is a source-of-truth for files extracted from the Archimedes retail/engineering firmware and for the makefiles that expose them to an Android build.

## Scope

- Device path: `vendor/xiaomi/archimedes`
- Platform: MediaTek MT6761
- Main use: 64-bit user space with the Archimedes vendor stack
- IMS work: preserve the stock MTK RIL/IMS/modem interface and record carrier-specific behavior separately

The repository will eventually contain the complete Archimedes ALPS vendor side. Until every file has a verified source, the manifest is kept explicit and incomplete rather than filled with guessed paths.

## Layout

```text
Android.mk                    top-level vendor include
BoardConfigVendor.mk          board-specific vendor flags
archimedes-vendor.mk          generated PRODUCT_COPY_FILES
proprietary-files.txt         reviewed extraction manifest
proprietary/                  extracted files, preserving vendor paths
metadata/                     source, build, hash, and partition records
scripts/extract-files.sh      reproducible extraction entry point
scripts/setup-makefiles.sh    makefile generation entry point
tools/                        host-side helpers
```

## Extraction rules

Only files from `system`, `system_ext`, `product`, `vendor`, `odm`, and the firmware package may be considered. Do not copy these into the repository:

- `nvram`, `nvdata`, `protect`, `persist`, or any IMEI/calibration data
- live modem runtime state or user data
- full partition images unless a release specifically requires one
- private keys, device certificates, or account data

Every imported file must have a source record and SHA-256 in `metadata/`. The source record must identify the firmware build, partition, path, extraction date, and whether the file is 32-bit or 64-bit.

## Basic use

From a Lineage/AOSP tree:

```sh
./vendor/xiaomi/archimedes/scripts/setup-makefiles.sh
```

For a device connected with elevated ADB:

```sh
./vendor/xiaomi/archimedes/scripts/extract-files.sh --adb
```

The extractor reads `proprietary-files.txt`, writes into `proprietary/`, and updates the metadata manifest. It never reads NVRAM or calibration partitions.

## Current status

The `main` branch now contains a regular-file snapshot of the connected
Archimedes vendor partition, including the MTK RIL/IMS, Wi-Fi/Bluetooth,
camera, audio, display, sensor, firmware, and kernel-module files currently
visible to the target system. The snapshot is tagged in
`metadata/source-device.txt` and every file has a SHA-256 row in
`metadata/extracted-files.tsv`.

This is a device snapshot, not yet a clean Redmi 6A donor merge. The next
comparison source is the Redmi 6A stock vendor/modem stack; files are merged
only after their ABI, SELinux context, architecture, and firmware provenance
are reviewed. Debug-only files present on the target snapshot must be reviewed
before they are used as a release baseline.

## License

The makefiles and scripts are Apache-2.0 unless stated otherwise. Extracted vendor binaries remain under their original copyright and license terms; this repository does not relicense them.
