<h1 align="center">Apps Repository</h1>

<div align="center">

<p><i>Official signed package repository and update backend for the LineageOS App Store.</i></p>

[![LineageOS](https://img.shields.io/badge/LineageOS-167C80?style=for-the-badge&logo=lineageos&logoColor=white)](https://lineageos.org/)
[![Repository](https://img.shields.io/badge/Repository-Backend-0969DA?style=for-the-badge&logo=github&logoColor=white)](#)
[![Ed25519](https://img.shields.io/badge/Signify-Ed25519-005FB8?style=for-the-badge&logo=gnuprivacyguard&logoColor=white)](#)
[![Active](https://img.shields.io/badge/Status-Active-2EA44F?style=for-the-badge)](#)

</div>

## About

This repository hosts the signed application metadata catalog, split APKs, and distribution releases for the **App Store** ecosystem on LineageOS devices.

It is served statically via GitHub Pages at [`https://rhythmcreative.github.io/apps-repository`](https://rhythmcreative.github.io/apps-repository) and cryptographically authenticated against our root Ed25519 public key.

## Managed Packages

| Package Name | Application | Channel | Provider |
| :--- | :--- | :--- | :--- |
| `io.github.jqssun.helium` | Titanium Browser | Stable / Alpha | [jqssun/android-titanium-browser](https://github.com/jqssun/android-titanium-browser) |
| `org.lineageos.info` | LineageOS Info | Stable / Alpha | [rhythmcreative/Info](https://github.com/rhythmcreative/Info) |
| `com.android.vending` | Google Play Store | Stable / Alpha | Google (Official Verified) |
| `com.google.android.gms` | Google Play Services | Stable / Alpha | Google (Official Verified) |
| `com.google.android.gsf` | Google Services Framework | Stable / Alpha | Google (Official Verified) |
| `com.google.android.projection.gearhead` | Android Auto | Stable / Alpha | Google (Official Verified) |

## Repository Structure

```text
.
├── apps/
│   └── packages/
│       ├── io.github.jqssun.helium/
│       ├── org.lineageos.info/
│       ├── com.android.vending/
│       ├── com.google.android.gms/
│       └── com.google.android.gsf/
├── generate.py
├── import-apks.py
├── compress-apks
└── static/
```

## Security & Verification

All repository metadata files (`metadata.1.0.sjson`) are signed with an Ed25519 keypair using `signify`. The public key is compiled into the client app, preventing untrusted package installations or tampering:

- **Public Key:** `RWQevdGSdsZc6yuJKy+CnCqhHTqqyjGTDsgtAxWzrCBGpROXDJEe6Znz`
- **Verification:** Signed using `signify` scheme (`apps.0.pub` / `apps.0.sec`)

## Generating Catalog

```bash
./generate.py
```

## Disclaimer

This is an unofficial repository for distributing verified applications on LineageOS. Not affiliated with Google or GrapheneOS.

<div align="center">

<p>Made with ❤️ from rhythmcreative.</p>

</div>
