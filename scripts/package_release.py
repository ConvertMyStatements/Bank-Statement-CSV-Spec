#!/usr/bin/env python3
"""Create zip bundles for GitHub Releases."""
from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "samples"
RELEASE_DIR = ROOT / "releases"
CHECKSUMS = ROOT / "checksums.txt"
MANIFEST = ROOT / "MANIFEST.json"


def zip_files(target: Path, files: Iterable[Path]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(files, key=lambda p: p.as_posix()):
            archive.write(file_path, file_path.relative_to(ROOT))


def iter_sample_files() -> Iterable[Path]:
    for path in sorted(SAMPLES_DIR.glob("**/*.csv"), key=lambda p: p.as_posix()):
        yield path


def package_per_software() -> list[Path]:
    bundles = []
    for software_dir in sorted(SAMPLES_DIR.iterdir()):
        if not software_dir.is_dir() or software_dir.name == "edge-cases":
            continue
        files = sorted(software_dir.glob("**/*.csv"), key=lambda p: p.as_posix())
        if not files:
            continue
        zip_path = RELEASE_DIR / f"{software_dir.name}-all-locales.zip"
        zip_files(zip_path, files)
        bundles.append(zip_path)
    return bundles


def package_per_locale() -> list[Path]:
    bundles = []
    locales = {}
    for csv_path in iter_sample_files():
        parts = csv_path.relative_to(SAMPLES_DIR).parts
        if parts[0] == "edge-cases":
            continue
        software, locale = parts[0], parts[1]
        locales.setdefault(locale, []).append(csv_path)
    for locale in sorted(locales.keys()):
        files = sorted(locales[locale], key=lambda p: p.as_posix())
        zip_path = RELEASE_DIR / f"locale-{locale}.zip"
        zip_files(zip_path, files)
        bundles.append(zip_path)
    return bundles


def package_edge_cases() -> Path | None:
    edge_dir = SAMPLES_DIR / "edge-cases"
    if not edge_dir.exists():
        return None
    files = sorted(edge_dir.glob("*.csv"), key=lambda p: p.as_posix())
    if not files:
        return None
    zip_path = RELEASE_DIR / "edge-cases.zip"
    zip_files(zip_path, files)
    return zip_path


def copy_reference_files() -> list[Path]:
    reference = []
    for path in (CHECKSUMS, MANIFEST):
        if path.exists():
            target = RELEASE_DIR / path.name
            target.write_bytes(path.read_bytes())
            reference.append(target)
    return reference


def main() -> None:
    if RELEASE_DIR.exists():
        for item in RELEASE_DIR.glob("*"):
            if item.is_file():
                item.unlink()
    release_files = []
    release_files.extend(package_per_software())
    release_files.extend(package_per_locale())
    edge = package_edge_cases()
    if edge:
        release_files.append(edge)
    release_files.extend(copy_reference_files())
    print("Release bundles ready:")
    for file_path in release_files:
        print(f" - {file_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
