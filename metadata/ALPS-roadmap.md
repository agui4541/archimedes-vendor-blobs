# ALPS integration roadmap

This repository is the proprietary vendor layer for Archimedes. It is deliberately
kept separate from the MTK ALPS source tree so that open-source framework code,
GPL obligations, and redistributable device blobs remain reviewable independently.

## Stages

1. **Donor inventory** — extract Redmi 6A stock `vendor`, `odm`, `system`,
   `system_ext`, `product`, and firmware files. Record build fingerprint,
   partition origin, architecture, SHA-256, SELinux context, and dependencies.
2. **Archimedes delta** — compare those files with the retail and engineering
   Archimedes images. Keep only files required for MT6761 hardware, RIL/IMS,
   Wi-Fi/Bluetooth, camera, audio, sensors, and display operation.
3. **Generated build layer** — add reviewed paths to `proprietary-files.txt` and
   regenerate `archimedes-vendor.mk`; never hand-edit generated output.
4. **ALPS framework** — maintain the matching open-source MTK ALPS base in its
   own source tree, then add Archimedes device configuration and overlays here.
5. **Reproducible builds** — validate extraction metadata and generated makefiles
   in CI before publishing a vendor revision.

NVRAM, NVDATA, protect/persist partitions, IMEI, calibration, and user data are
never part of this repository. They stay in a separately controlled, device-
specific backup process.
