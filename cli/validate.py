#!/usr/bin/env python3
"""Friendly CSV validator that mirrors the ConvertMyStatements web checks."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

CONFIG_DEFAULT = Path(__file__).resolve().parents[1] / "schema" / "validator-config.json"
CTA_LINK = "https://www.convertmystatements.com/specs/bank-statement-csv#validator?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec"


class ValidationIssue:
    def __init__(self, code: str, message: str, hint: str) -> None:
        self.code = code
        self.message = message
        self.hint = hint

    def __str__(self) -> str:
        return f"{self.message} — {self.hint}"


def load_config(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        sys.exit(f"Config file not found at {path}. Download the latest repo bundle or run from the project root.")


def read_csv(path: Path) -> List[Dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
    except FileNotFoundError:
        sys.exit(f"We couldn’t find {path}. Drag & drop the file onto this script or run it again with the correct path.")
    except UnicodeDecodeError:
        sys.exit("The file isn’t UTF-8. Re-save it as 'CSV UTF-8 (Comma delimited)' and try again.")

    if not rows:
        sys.exit("The CSV is empty. Export a fresh file or download a sample from the Releases tab.")

    return rows


def ensure_columns(rows: List[Dict[str, str]], config: Dict[str, Any]) -> List[ValidationIssue]:
    header = rows[0].keys()
    issues: List[ValidationIssue] = []
    missing = [col for col in config["required_columns"] if col not in header]
    if missing:
        issues.append(
            ValidationIssue(
                "CSV001",
                f"Missing column(s): {', '.join(missing)}",
                "Match the headers from the sample files exactly."
            )
        )
    return issues


def validate_dates(rows: List[Dict[str, str]], allowed_formats: Iterable[str]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    for idx, row in enumerate(rows, start=2):  # +2 for header row
        raw_date = row.get("transaction_date", "").strip()
        if not raw_date:
            issues.append(
                ValidationIssue(
                    "CSV002",
                    f"Row {idx}: transaction_date is blank",
                    "Fill every date. Use the bank statement’s original date format."
                )
            )
            continue
        parsed = False
        for fmt in allowed_formats:
            try:
                datetime.strptime(raw_date, fmt)
                parsed = True
                break
            except ValueError:
                continue
        if not parsed:
            display = " or ".join(fmt.replace("%Y", "YYYY").replace("%m", "MM").replace("%d", "DD") for fmt in allowed_formats)
            issues.append(
                ValidationIssue(
                    "CSV004",
                    f"Row {idx}: transaction_date '{raw_date}' doesn't match {display}",
                    "Align the date format with the sample for your software."
                )
            )
    return issues


def validate_amounts(rows: List[Dict[str, str]], pattern: str, decimal_separator: str) -> List[ValidationIssue]:
    import re

    regex = re.compile(pattern)
    issues: List[ValidationIssue] = []
    for idx, row in enumerate(rows, start=2):
        amount = row.get("amount", "").strip()
        if not amount:
            issues.append(
                ValidationIssue(
                    "CSV005",
                    f"Row {idx}: amount is blank",
                    "Populate every amount. Use positive numbers only; debit/credit decides the direction."
                )
            )
            continue
        if decimal_separator == ",":
            candidate = amount.replace(".", "").replace(",", ".")
        else:
            candidate = amount
        if not regex.match(candidate):
            issues.append(
                ValidationIssue(
                    "CSV006",
                    f"Row {idx}: amount '{amount}' is not formatted correctly",
                    f"Use two decimal places (e.g., 1234{decimal_separator}56) and remove currency symbols."
                )
            )
    return issues


def validate_debit_credit(rows: List[Dict[str, str]], allowed: Iterable[str]) -> List[ValidationIssue]:
    allowed_set = {value.lower() for value in allowed}
    issues: List[ValidationIssue] = []
    for idx, row in enumerate(rows, start=2):
        value = row.get("debit_credit", "").strip().lower()
        if value not in allowed_set:
            issues.append(
                ValidationIssue(
                    "CSV008",
                    f"Row {idx}: debit_credit '{row.get('debit_credit', '')}' is not one of {', '.join(allowed)}",
                    "Set to 'debit' for money out and 'credit' for money in."
                )
            )
    return issues


def validate_currency(rows: List[Dict[str, str]], allowed: Iterable[str]) -> List[ValidationIssue]:
    allowed_set = set(allowed)
    issues: List[ValidationIssue] = []
    for idx, row in enumerate(rows, start=2):
        value = row.get("currency", "").strip().upper()
        if value and value not in allowed_set:
            issues.append(
                ValidationIssue(
                    "CSV022",
                    f"Row {idx}: currency '{value}' is outside the allowed list",
                    f"Stick to {', '.join(sorted(allowed_set))}. Separate files per currency."
                )
            )
    return issues


def validate_unique_ids(rows: List[Dict[str, str]]) -> List[ValidationIssue]:
    ids = [row.get("unique_id", "").strip() for row in rows]
    duplicates = [item for item, count in Counter(ids).items() if item and count > 1]
    if not duplicates:
        return []
    dup_display = ", ".join(duplicates[:3]) + ("…" if len(duplicates) > 3 else "")
    return [
        ValidationIssue(
            "CSV010",
            f"Found duplicate unique_id values: {dup_display}",
            "Ensure each transaction ID is unique; copy the structure from our samples if needed."
        )
    ]


def summarise(issues: List[ValidationIssue], profile_label: str, file_path: Path) -> None:
    if not issues:
        print("✅ All good! This file matches the ConvertMyStatements checks.")
        print(f"Profile: {profile_label}")
        print("Tip: keep a copy of this CSV alongside your workpapers and note the validator timestamp.")
        print(f"Need the hosted version? {CTA_LINK}")
        return

    print("⚠️ Needs attention — we spotted a few fixes to make before importing.")
    print(f"Profile: {profile_label}")
    print("")
    for issue in issues:
        print(f"• [{issue.code}] {issue.message}\n    ↳ {issue.hint}")
    print("")
    print("Download a fresh sample or use the hosted validator for step-by-step guidance:")
    print(CTA_LINK)
    print("")
    print("Once adjusted, re-run this script or upload the file again to confirm the fixes.")

    # Exit with non-zero code for automation contexts
    sys.exit(1)


def prompt_for_file() -> Path:
    try:
        answer = input("Drag & drop your CSV here (or type the path) and press Enter:\n> ").strip().strip('"')
    except EOFError:
        sys.exit("No file provided. Run the script again and drop the CSV onto it.")
    if not answer:
        sys.exit("No file provided. Run the script again and drop the CSV onto it.")
    return Path(answer)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Validate bank statement CSVs before importing them into your accounting software.",
        add_help=True,
    )
    parser.add_argument("csv_path", nargs="?", help="Path to the CSV file you want to check")
    parser.add_argument("--profile", default="quickbooks-us", help="Validation profile (defaults to quickbooks-us)")
    parser.add_argument("--config", default=str(CONFIG_DEFAULT), help="Override the config file path if needed")

    args = parser.parse_args(argv)

    csv_path = Path(args.csv_path) if args.csv_path else prompt_for_file()
    config_path = Path(args.config)
    config = load_config(config_path)

    profile_key = args.profile
    profiles = config.get("profiles", {})
    if profile_key not in profiles:
        available = ", ".join(sorted(profiles.keys()))
        sys.exit(f"Unknown profile '{profile_key}'. Available options: {available}")

    profile = profiles[profile_key]
    rows = read_csv(csv_path)

    issues: List[ValidationIssue] = []
    issues.extend(ensure_columns(rows, config))
    issues.extend(validate_dates(rows, profile.get("date_format", [])))
    issues.extend(validate_amounts(rows, config["amount_pattern"], profile.get("decimal_separator", ".")))
    issues.extend(validate_debit_credit(rows, config["allowed_debit_credit"]))
    issues.extend(validate_currency(rows, profile.get("currency", [])))
    issues.extend(validate_unique_ids(rows))

    summarise(issues, profile.get("label", profile_key), csv_path)


if __name__ == "__main__":
    main()
