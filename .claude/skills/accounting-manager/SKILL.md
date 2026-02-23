# Accounting Manager Agent Skill

## Overview

The Accounting Manager skill maintains financial records in the AI Employee vault, tracking income and expenses with automatic weekly summaries and totals.

## Capabilities

1. **Transaction Logging**
   - Log income and expense transactions
   - Maintain Current_Month.md file
   - Structured format with date, type, amount, description

2. **Financial Summaries**
   - Generate weekly summaries
   - Calculate total income
   - Calculate total expenses
   - Calculate net profit/loss

3. **Automated Reporting**
   - Weekly financial reports
   - Monthly summaries
   - Transaction categorization

## Usage

### Trigger Phrases

When the user says any of these, invoke this skill:

- "Log a transaction"
- "Add income"
- "Add expense"
- "Record payment"
- "Track spending"
- "Show financial summary"
- "Generate accounting report"
- "What's my income this month?"
- "What are my expenses?"
- "Show me the weekly summary"

### Skill Invocation

```bash
# Log a transaction
python scripts/accounting_manager.py log --type income --amount 1500 --description "Client A payment for Project Alpha"

# Log an expense
python scripts/accounting_manager.py log --type expense --amount 250 --description "Software subscription - Adobe Creative Cloud"

# Generate weekly summary
python scripts/accounting_manager.py summary --period week

# Generate monthly summary
python scripts/accounting_manager.py summary --period month

# Show current totals
python scripts/accounting_manager.py totals
```

## File Structure

### Current_Month.md Format

```markdown
# Financial Records - February 2026

## Transactions

| Date       | Type    | Amount  | Description                           |
|------------|---------|---------|---------------------------------------|
| 2026-02-01 | Income  | $1,500  | Client A payment for Project Alpha    |
| 2026-02-03 | Expense | $250    | Software subscription - Adobe         |
| 2026-02-05 | Income  | $2,000  | Client B - Website development        |
| 2026-02-07 | Expense | $150    | Marketing - LinkedIn ads              |

## Weekly Summary (Week 1: Feb 1-7)

- **Total Income**: $3,500
- **Total Expenses**: $400
- **Net Profit**: $3,100

## Monthly Totals

- **Total Income**: $3,500
- **Total Expenses**: $400
- **Net Profit**: $3,100
- **Transaction Count**: 4

---
Last updated: 2026-02-07 14:30:00
```

## Workflow

### 1. Transaction Logging

When a transaction needs to be logged:

1. User provides transaction details (type, amount, description)
2. Skill validates the input
3. Appends transaction to Current_Month.md
4. Updates monthly totals
5. Logs activity to business.log

### 2. Weekly Summary Generation

Every Sunday or on-demand:

1. Calculate transactions for the current week
2. Sum income and expenses
3. Calculate net profit/loss
4. Update Current_Month.md with weekly summary

### 3. Monthly Summary

At month end or on-demand:

1. Calculate all transactions for the month
2. Generate comprehensive summary
3. Archive to AI_Employee_Vault/Accounting/Archive/YYYY-MM.md
4. Create new Current_Month.md for next month

## Integration Points

### With Other Skills

- **gmail-send**: Email monthly reports to accountant
- **human-approval**: Request approval for large expenses
- **vault-file-manager**: Archive old accounting files

### With MCP Server

- **log_activity**: All transactions logged to business.log
- **send_email**: Send financial reports via email

## Security

- All financial data stored locally in vault
- No external API calls for sensitive data
- Audit trail in business.log
- Human approval required for transactions over threshold

## Configuration

Set these environment variables (optional):

```bash
# Approval threshold for large transactions
export ACCOUNTING_APPROVAL_THRESHOLD=500

# Currency symbol
export ACCOUNTING_CURRENCY="$"

# Week start day (0=Sunday, 1=Monday)
export ACCOUNTING_WEEK_START=1
```

## Examples

### Example 1: Log Client Payment

```bash
python scripts/accounting_manager.py log \
  --type income \
  --amount 2500 \
  --description "Client C - Q1 Consulting Services"
```

**Output:**
```json
{
  "success": true,
  "message": "Transaction logged successfully",
  "transaction": {
    "date": "2026-02-23",
    "type": "income",
    "amount": 2500,
    "description": "Client C - Q1 Consulting Services"
  },
  "new_totals": {
    "income": 6000,
    "expenses": 400,
    "net": 5600
  }
}
```

### Example 2: Log Business Expense

```bash
python scripts/accounting_manager.py log \
  --type expense \
  --amount 89.99 \
  --description "Office supplies - Staples"
```

### Example 3: Generate Weekly Summary

```bash
python scripts/accounting_manager.py summary --period week
```

**Output:**
```json
{
  "success": true,
  "period": "Week 4: Feb 17-23, 2026",
  "income": 2500,
  "expenses": 89.99,
  "net": 2410.01,
  "transaction_count": 2
}
```

### Example 4: Show Monthly Totals

```bash
python scripts/accounting_manager.py totals
```

**Output:**
```json
{
  "success": true,
  "month": "February 2026",
  "total_income": 6000,
  "total_expenses": 489.99,
  "net_profit": 5510.01,
  "transaction_count": 6
}
```

## Error Handling

The skill handles common errors gracefully:

- Invalid transaction type (must be income or expense)
- Invalid amount (must be positive number)
- Missing description
- File access errors
- Corrupted accounting file

All errors return structured JSON with error details.

## Automation

### Scheduled Tasks

Add to `scripts/scheduler.py`:

```python
# Generate weekly summary every Sunday at 8 PM
schedule.every().sunday.at("20:00").do(
    lambda: subprocess.run([
        "python", "scripts/accounting_manager.py",
        "summary", "--period", "week"
    ])
)

# Archive monthly records on the 1st of each month
schedule.every().day.at("00:01").do(check_and_archive_month)
```

## Best Practices

1. **Log transactions immediately** - Don't wait, log as they happen
2. **Use descriptive descriptions** - Include client names, project details
3. **Review weekly summaries** - Check for accuracy every week
4. **Archive monthly** - Keep Current_Month.md manageable
5. **Backup regularly** - Git commit accounting files frequently

## Troubleshooting

### Issue: Totals don't match

**Solution:** Run validation command
```bash
python scripts/accounting_manager.py validate
```

### Issue: Missing transactions

**Solution:** Check business.log for audit trail
```bash
tail -n 50 AI_Employee_Vault/Logs/business.log | grep "Transaction logged"
```

### Issue: File corrupted

**Solution:** Restore from git history
```bash
git checkout HEAD~1 -- AI_Employee_Vault/Accounting/Current_Month.md
```

## Future Enhancements

- Category tagging (e.g., #software, #marketing, #client-work)
- Multi-currency support
- Tax calculation and reporting
- Integration with Odoo accounting (Gold Tier)
- Automatic bank transaction import
- Receipt attachment support

---

**Skill Type:** Agent Skill (Local Execution)
**Dependencies:** Python 3.13+, scripts/accounting_manager.py
**Security Level:** High (financial data)
**Approval Required:** For transactions > $500
