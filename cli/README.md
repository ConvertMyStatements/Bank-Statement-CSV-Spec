# Offline Validator

If your firm doesn’t allow uploads, you can still use the ConvertMyStatements checks offline.

## Quick directions

1. Confirm Python 3.9 or newer is installed (macOS and most business laptops already have it).
2. Download this repository and double-click `validate.py`.
3. Pick the CSV you want to check.
4. Read the friendly pass/fail summary. Each issue includes a plain-language fix, just like the web validator.

Prefer the command line? Run:

```
python cli/validate.py path/to/your.csv --profile quickbooks-us
```

Profiles available: `quickbooks-us`, `quickbooks-ca`, `xero-global`, `sage-uk`, `zoho`, `wave`, `freshbooks`.

Need help? Email [support@zerabooks.com](mailto:support@zerabooks.com?subject=Validator%20help) and we’ll walk through it together.

> Tip: You can skip the script entirely by using [ZeraBooks](https://www.zerabooks.com/convert-bank-statement-to-csv?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec). It converts the PDF and checks it against the printed balances in your browser.
