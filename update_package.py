#!/usr/bin/env python3
import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

def get_apk_info(apk_path):
    aapt2 = shutil.which("aapt2")
    if not aapt2:
        default_sdk = "/home/rhythmcreative/Android/Sdk/build-tools/36.0.0/aapt2"
        if os.path.exists(default_sdk):
            aapt2 = default_sdk
        else:
            found = shutil.which("aapt")
            if found:
                aapt2 = found
            else:
                raise FileNotFoundError("aapt2 not found in PATH or Android SDK")

    out = subprocess.check_output([aapt2, "dump", "badging", apk_path], text=True, stderr=subprocess.DEVNULL)
    pkg_match = re.search(r"package:\s+name='([^']+)'\s+versionCode='([^']+)'\s+versionName='([^']*)'", out)
    if not pkg_match:
        raise ValueError("Could not parse package info from APK")
    
    pkg_name = pkg_match.group(1)
    version_code = int(pkg_match.group(2))
    version_name = pkg_match.group(3)

    min_sdk_match = re.search(r"minSdkVersion:'([^']+)'", out)
    min_sdk = int(min_sdk_match.group(1)) if min_sdk_match else 29

    label_match = re.search(r"application-label:'([^']+)'", out) or re.search(r"application:\s+label='([^']+)'", out)
    label = label_match.group(1) if label_match else pkg_name

    with open(apk_path, "rb") as f:
        content = f.read()

    sha256 = hashlib.sha256(content).hexdigest()
    apk_size = len(content)
    gz_content = gzip.compress(content, compresslevel=9)
    gz_size = len(gz_content)

    return {
        "packageName": pkg_name,
        "versionCode": version_code,
        "versionName": version_name,
        "minSdk": min_sdk,
        "label": label,
        "sha256": sha256,
        "size": apk_size,
        "gzSize": gz_size,
    }

def sign_metadata(metadata_json_path, key_path, sjson_path):
    sig_file = metadata_json_path + ".0.sig"
    cmd = ["signify", "-S", "-s", key_path, "-m", metadata_json_path, "-x", sig_file]
    subprocess.check_call(cmd)

    with open(sig_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        sig = lines[1]

    shutil.copy(metadata_json_path, sjson_path)
    with open(sjson_path, "a") as f:
        f.write("\n" + sig + "\n")
    print(f"Successfully signed {sjson_path}")

def main():
    parser = argparse.ArgumentParser(description="Update and sign package in App Store catalog")
    parser.add_argument("apk", help="Path to the new APK file")
    parser.add_argument("--url", help="Download URL (e.g. GitHub Releases URL)")
    parser.add_argument("--channel", default="stable", help="Release channel (default: stable)")
    parser.add_argument("--key", default="/home/rhythmcreative/.android-certs/apps.0.sec", help="Signify private key")
    parser.add_argument("--repo-dir", default=os.path.dirname(os.path.abspath(__file__)), help="Directory containing metadata.1.json")
    args = parser.parse_args()

    info = get_apk_info(args.apk)
    pkg_name = info["packageName"]
    version_code = str(info["versionCode"])

    metadata_path = os.path.join(args.repo_dir, "metadata.1.json")
    sjson_path = os.path.join(args.repo_dir, "metadata.1.0.sjson")

    with open(metadata_path, "r") as f:
        catalog = json.load(f)

    if pkg_name not in catalog["packages"]:
        catalog["packages"][pkg_name] = {
            "source": "GrapheneOS",
            "variants": {}
        }

    pkg_entry = catalog["packages"][pkg_name]
    if "variants" not in pkg_entry:
        pkg_entry["variants"] = {}

    variant = {
        "versionCode": info["versionCode"],
        "apks": ["base.apk"],
        "apkHashes": [info["sha256"]],
        "apkSizes": [info["size"]],
        "apkGzSizes": [info["gzSize"]],
        "apkBrSizes": [info["gzSize"]],
        "versionName": info["versionName"],
        "minSdk": info["minSdk"],
        "label": info["label"],
        "channel": args.channel
    }

    if args.url:
        variant["apkUrls"] = [args.url]

    pkg_entry["variants"][version_code] = variant
    print(f"Updated {pkg_name} to version {info['versionName']} (code {version_code})")

    # Compact dump without trailing newline
    with open(metadata_path, "w") as f:
        json.dump(catalog, f, separators=(",", ":"))

    sign_metadata(metadata_path, args.key, sjson_path)

if __name__ == "__main__":
    main()
