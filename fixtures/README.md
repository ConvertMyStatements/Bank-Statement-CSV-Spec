# Fixture Templates

Fixtures describe each sample CSV in plain language so you can edit or extend the library without touching spreadsheets.

Key fields:

- `bank`: Friendly bank name (e.g., "Chase").
- `country`: Two-letter country code.
- `software`: One of the six supported import tools.
- `account_type`: Checking, savings, credit_card, or mixed.
- `currency`: ISO 4217 code.
- `date_format`: Matches the bank statement ("YYYY-MM-DD", "DD/MM/YYYY", etc.).
- `decimal_separator`: `.` or `,`.
- `rows`: A short list of representative transactions.

Update a fixture, run the generator, and the matching CSV in `/samples/` will refresh automatically. When in doubt, upload the original PDF to [ConvertMyStatements](https://www.convertmystatements.com/?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec) and we’ll build the sample for you.
