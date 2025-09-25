#!/usr/bin/env python3
"""Generate CSV samples, manifest, and checksum file from fixtures."""
from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = ROOT / "fixtures"
SAMPLES_DIR = ROOT / "samples"
EDGE_DIR = FIXTURES_DIR / "edge"
MANIFEST_PATH = ROOT / "MANIFEST.json"
CHECKSUMS_PATH = ROOT / "checksums.txt"

STANDARD_COLUMNS = [
    "transaction_date",
    "description",
    "amount",
    "debit_credit",
    "balance",
    "currency",
    "unique_id",
    "memo",
]


def format_decimal(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text())


def iter_bank_fixtures() -> Iterable[Path]:
    paths = sorted(
        (path for path in FIXTURES_DIR.glob("*/*.yaml") if path.parent.name != "edge"),
        key=lambda p: (p.parent.name, p.name),
    )
    for path in paths:
        yield path


def write_csv(path: Path, headers: Iterable[str], rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(headers))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def checksum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_standard_row(raw: Dict[str, Any], currency: str) -> Dict[str, Any]:
    return {
        "transaction_date": raw.get("transaction_date", ""),
        "description": raw.get("description", ""),
        "amount": format_decimal(raw.get("amount")),
        "debit_credit": raw.get("debit_credit", ""),
        "balance": format_decimal(raw.get("balance")),
        "currency": currency,
        "unique_id": raw.get("unique_id", ""),
        "memo": raw.get("memo", ""),
    }


def generate_samples() -> Dict[str, Any]:
    manifest_records = []

    for fixture_path in iter_bank_fixtures():
        fixture = load_yaml(fixture_path)
        bank = fixture["bank"]
        country = fixture["country"]
        software_profiles = fixture["software_profiles"]
        currency = fixture["currency"]
        locale = fixture["locale"]
        account_type = fixture["account_type"]

        for software_id in sorted(software_profiles.keys()):
            profile = software_profiles[software_id]
            rows = [build_standard_row(row, currency) for row in fixture["rows"]]
            folder = profile["folder"]
            region_code = country["code"].lower()
            filename = f"{bank['slug']}__{software_id}__{profile['filename_suffix']}.csv"
            output_path = SAMPLES_DIR / folder / region_code / filename
            write_csv(output_path, STANDARD_COLUMNS, rows)
            sha = checksum(output_path)
            manifest_records.append(
                {
                    "bank": bank["name"],
                    "bank_slug": bank["slug"],
                    "country_code": country["code"],
                    "software": software_id,
                    "software_profile": profile["profile"],
                    "path": str(output_path.relative_to(ROOT)).replace("\\", "/"),
                    "checksum_sha256": sha,
                    "currency": currency,
                    "locale": locale,
                    "account_type": account_type,
                }
            )

    manifest_records.sort(key=lambda item: (item["software"], item["country_code"], item["bank_slug"], item["path"]))
    return {
        "samples": manifest_records,
    }


def generate_edge_cases() -> list[Dict[str, Any]]:
    edge_records = []
    for edge_fixture in sorted(EDGE_DIR.glob("*.yaml")):
        data = load_yaml(edge_fixture)
        scenario = data["scenario"]
        rows = data.get("rows", [])
        currency = data.get("currency", "")
        headers = list({key for row in rows for key in row.keys()})
        # Ensure standard headers appear first for familiarity
        ordered_headers = [col for col in STANDARD_COLUMNS if col in headers]
        for key in headers:
            if key not in ordered_headers:
                ordered_headers.append(key)

        csv_rows = []
        for row in rows:
            csv_row = {col: "" for col in ordered_headers}
            for key, value in row.items():
                if key == "amount":
                    csv_row[key] = format_decimal(value)
                elif key == "balance":
                    csv_row[key] = format_decimal(value)
                elif key == "currency" and not value:
                    csv_row[key] = currency
                else:
                    csv_row[key] = value
            if currency and "currency" in ordered_headers and not csv_row.get("currency"):
                csv_row["currency"] = currency
            csv_rows.append(csv_row)

        output_path = SAMPLES_DIR / "edge-cases" / f"edge-{scenario}.csv"
        write_csv(output_path, ordered_headers, csv_rows)
        sha = checksum(output_path)
        edge_records.append(
            {
                "scenario": scenario,
                "description": data.get("description", ""),
                "expected_error": data.get("expected_error", ""),
                "path": str(output_path.relative_to(ROOT)).replace("\\", "/"),
                "checksum_sha256": sha,
            }
        )
    edge_records.sort(key=lambda item: item["scenario"])
    return edge_records


def update_manifest(
    sample_data: Dict[str, Any],
    edge_records: list[Dict[str, Any]],
    existing: Dict[str, Any] | None,
    preserve_timestamp: bool,
) -> Dict[str, Any]:
    previous_generated_at = None
    if preserve_timestamp and existing:
        previous_generated_at = existing.get("generated_at")

    manifest = {
        "version": "1.0.0-draft",
        "generated_at": previous_generated_at
        or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "summary": {
            "total_samples": len(sample_data["samples"]),
            "total_edge_cases": len(edge_records),
            "softwares": sorted({item["software"] for item in sample_data["samples"]}),
            "countries": sorted({item["country_code"] for item in sample_data["samples"]}),
        },
        "samples": sample_data["samples"],
        "edge_cases": edge_records,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    return manifest


def write_checksums(records: Iterable[Dict[str, Any]]) -> None:
    lines = []
    for record in records:
        lines.append(f"{record['checksum_sha256']}  {record['path']}")
    lines.sort()
    CHECKSUMS_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    preserve_timestamp = os.getenv("CI", "").lower() == "true"
    existing_manifest: Dict[str, Any] | None = None
    if MANIFEST_PATH.exists():
        try:
            existing_manifest = json.loads(MANIFEST_PATH.read_text())
        except json.JSONDecodeError:
            existing_manifest = None

    if SAMPLES_DIR.exists():
        # Clean previous generated CSVs
        for csv_path in SAMPLES_DIR.glob("**/*.csv"):
            csv_path.unlink()
    sample_data = generate_samples()
    edge_records = generate_edge_cases()
    manifest = update_manifest(sample_data, edge_records, existing_manifest, preserve_timestamp)
    write_checksums(manifest["samples"] + edge_records)
    print(f"Generated {len(manifest['samples'])} samples and {len(edge_records)} edge cases.")
    print(f"Manifest updated at {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Checksums written to {CHECKSUMS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
