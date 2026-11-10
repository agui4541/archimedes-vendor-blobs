# Source records for extracted files

Each row should include:

- firmware/build identifier
- partition (`system`, `vendor`, `odm`, etc.)
- original path
- destination path
- SHA-256
- architecture (`32`, `64`, or `both`)
- extraction date
- notes about ABI, SELinux label, and known dependencies

Do not store NVRAM, NVDATA, IMEI, calibration, or account data here.
