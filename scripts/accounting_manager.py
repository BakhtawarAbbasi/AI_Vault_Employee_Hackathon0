#!/usr/bin/env python3
"""
Accounting Manager Script
Maintains financial records in AI_Employee_Vault/Accounting/Current_Month.md
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re


# Configuration
VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "AI_Employee_Vault")
ACCOUNTING_PATH = os.path.join(VAULT_PATH, "Accounting")
CURRENT_MONTH_FILE = os.path.join(ACCOUNTING_PATH, "Current_Month.md")
ARCHIVE_PATH = os.path.join(ACCOUNTING_PATH, "Archive")
LOGS_PATH = os.path.join(VAULT_PATH, "Logs")

# Environment variables
APPROVAL_THRESHOLD = float(os.getenv('ACCOUNTING_APPROVAL_THRESHOLD', '500'))
CURRENCY = os.getenv('ACCOUNTING_CURRENCY', '$')
WEEK_START = int(os.getenv('ACCOUNTING_WEEK_START', '1'))  # 0=Sunday, 1=Monday


def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(ACCOUNTING_PATH, exist_ok=True)
    os.makedirs(ARCHIVE_PATH, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)


def log_to_business_log(message):
    """Log activity to business.log"""
    try:
        log_file = os.path.join(LOGS_PATH, "business.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(json.dumps({"warning": f"Failed to log to business.log: {str(e)}"}))


def initialize_current_month():
    """Initialize Current_Month.md if it doesn't exist"""
    if not os.path.exists(CURRENT_MONTH_FILE):
        now = datetime.now()
        month_name = now.strftime("%B %Y")

        content = f"""# Financial Records - {month_name}

## Transactions

| Date       | Type    | Amount  | Description                           |
|------------|---------|---------|---------------------------------------|

## Weekly Summaries

## Monthly Totals

- **Total Income**: {CURRENCY}0.00
- **Total Expenses**: {CURRENCY}0.00
- **Net Profit**: {CURRENCY}0.00
- **Transaction Count**: 0

---
Last updated: {now.strftime("%Y-%m-%d %H:%M:%S")}
"""

        with open(CURRENT_MONTH_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        log_to_business_log(f"Initialized accounting file for {month_name}")


def parse_current_month_file():
    """Parse Current_Month.md and extract transactions"""
    if not os.path.exists(CURRENT_MONTH_FILE):
        return []

    transactions = []

    with open(CURRENT_MONTH_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract transaction table
    lines = content.split('\n')
    in_table = False

    for line in lines:
        if line.startswith('| Date'):
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) == 4 and parts[0] and parts[0] != 'Date':
                try:
                    date_str = parts[0]
                    trans_type = parts[1].lower()
                    amount_str = parts[2].replace(CURRENCY, '').replace(',', '').strip()
                    description = parts[3]

                    transactions.append({
                        'date': date_str,
                        'type': trans_type,
                        'amount': float(amount_str),
                        'description': description
                    })
                except (ValueError, IndexError):
                    continue
        elif in_table and not line.startswith('|'):
            break

    return transactions


def calculate_totals(transactions):
    """Calculate total income, expenses, and net"""
    income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    net = income - expenses

    return {
        'income': income,
        'expenses': expenses,
        'net': net,
        'count': len(transactions)
    }


def get_week_range(date=None):
    """Get the start and end date of the week containing the given date"""
    if date is None:
        date = datetime.now()

    # Adjust to week start day
    days_since_week_start = (date.weekday() - WEEK_START) % 7
    week_start = date - timedelta(days=days_since_week_start)
    week_end = week_start + timedelta(days=6)

    return week_start, week_end


def get_week_number(date):
    """Get the week number within the month"""
    first_day = date.replace(day=1)
    days_offset = (date - first_day).days
    week_num = (days_offset // 7) + 1
    return week_num


def calculate_weekly_summary(transactions, week_start, week_end):
    """Calculate summary for a specific week"""
    week_transactions = [
        t for t in transactions
        if week_start.strftime("%Y-%m-%d") <= t['date'] <= week_end.strftime("%Y-%m-%d")
    ]

    return calculate_totals(week_transactions)


def log_transaction(trans_type, amount, description):
    """Log a new transaction"""
    ensure_directories()
    initialize_current_month()

    # Validate inputs
    if trans_type not in ['income', 'expense']:
        return {
            "success": False,
            "error": "Transaction type must be 'income' or 'expense'"
        }

    if amount <= 0:
        return {
            "success": False,
            "error": "Amount must be positive"
        }

    if not description:
        return {
            "success": False,
            "error": "Description is required"
        }

    # Check if approval needed
    if amount > APPROVAL_THRESHOLD:
        approval_msg = f"Transaction requires approval (amount: {CURRENCY}{amount:,.2f} > threshold: {CURRENCY}{APPROVAL_THRESHOLD:,.2f})"
        log_to_business_log(approval_msg)
        return {
            "success": False,
            "error": approval_msg,
            "requires_approval": True
        }

    # Read current file
    with open(CURRENT_MONTH_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add new transaction
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    new_row = f"| {date_str} | {trans_type.capitalize()} | {CURRENCY}{amount:,.2f} | {description} |"

    # Find the transaction table and insert
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and line.startswith('|---') and i > 0 and lines[i-1].startswith('| Date'):
            new_lines.append(new_row)
            inserted = True

    # Update totals
    transactions = parse_current_month_file()
    transactions.append({
        'date': date_str,
        'type': trans_type,
        'amount': amount,
        'description': description
    })

    totals = calculate_totals(transactions)

    # Update Monthly Totals section
    updated_content = '\n'.join(new_lines)
    updated_content = re.sub(
        r'## Monthly Totals\n\n.*?(?=\n---|\Z)',
        f"""## Monthly Totals

- **Total Income**: {CURRENCY}{totals['income']:,.2f}
- **Total Expenses**: {CURRENCY}{totals['expenses']:,.2f}
- **Net Profit**: {CURRENCY}{totals['net']:,.2f}
- **Transaction Count**: {totals['count']}

""",
        updated_content,
        flags=re.DOTALL
    )

    # Update timestamp
    updated_content = re.sub(
        r'Last updated:.*',
        f"Last updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        updated_content
    )

    # Write back
    with open(CURRENT_MONTH_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    # Log activity
    log_to_business_log(f"Transaction logged: {trans_type} {CURRENCY}{amount:,.2f} - {description}")

    return {
        "success": True,
        "message": "Transaction logged successfully",
        "transaction": {
            "date": date_str,
            "type": trans_type,
            "amount": amount,
            "description": description
        },
        "new_totals": {
            "income": totals['income'],
            "expenses": totals['expenses'],
            "net": totals['net']
        }
    }


def generate_summary(period='week'):
    """Generate financial summary for week or month"""
    ensure_directories()
    initialize_current_month()

    transactions = parse_current_month_file()

    if period == 'week':
        week_start, week_end = get_week_range()
        week_num = get_week_number(datetime.now())
        summary = calculate_weekly_summary(transactions, week_start, week_end)

        # Update Current_Month.md with weekly summary
        with open(CURRENT_MONTH_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        week_summary_text = f"""
### Week {week_num}: {week_start.strftime('%b %d')}-{week_end.strftime('%d, %Y')}

- **Total Income**: {CURRENCY}{summary['income']:,.2f}
- **Total Expenses**: {CURRENCY}{summary['expenses']:,.2f}
- **Net Profit**: {CURRENCY}{summary['net']:,.2f}
- **Transaction Count**: {summary['count']}
"""

        # Insert or update weekly summary
        if '## Weekly Summaries' in content:
            content = content.replace(
                '## Weekly Summaries',
                f"## Weekly Summaries{week_summary_text}"
            )

        with open(CURRENT_MONTH_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        log_to_business_log(f"Generated weekly summary: Week {week_num}")

        return {
            "success": True,
            "period": f"Week {week_num}: {week_start.strftime('%b %d')}-{week_end.strftime('%d, %Y')}",
            "income": summary['income'],
            "expenses": summary['expenses'],
            "net": summary['net'],
            "transaction_count": summary['count']
        }

    elif period == 'month':
        totals = calculate_totals(transactions)
        month_name = datetime.now().strftime("%B %Y")

        log_to_business_log(f"Generated monthly summary: {month_name}")

        return {
            "success": True,
            "period": month_name,
            "income": totals['income'],
            "expenses": totals['expenses'],
            "net": totals['net'],
            "transaction_count": totals['count']
        }

    else:
        return {
            "success": False,
            "error": "Period must be 'week' or 'month'"
        }


def show_totals():
    """Show current monthly totals"""
    ensure_directories()
    initialize_current_month()

    transactions = parse_current_month_file()
    totals = calculate_totals(transactions)
    month_name = datetime.now().strftime("%B %Y")

    return {
        "success": True,
        "month": month_name,
        "total_income": totals['income'],
        "total_expenses": totals['expenses'],
        "net_profit": totals['net'],
        "transaction_count": totals['count']
    }


def validate_file():
    """Validate Current_Month.md for consistency"""
    ensure_directories()
    initialize_current_month()

    transactions = parse_current_month_file()
    calculated_totals = calculate_totals(transactions)

    # Read stated totals from file
    with open(CURRENT_MONTH_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract stated totals
    income_match = re.search(r'\*\*Total Income\*\*:\s*\$?([\d,]+\.?\d*)', content)
    expenses_match = re.search(r'\*\*Total Expenses\*\*:\s*\$?([\d,]+\.?\d*)', content)

    stated_income = float(income_match.group(1).replace(',', '')) if income_match else 0
    stated_expenses = float(expenses_match.group(1).replace(',', '')) if expenses_match else 0

    is_valid = (
        abs(stated_income - calculated_totals['income']) < 0.01 and
        abs(stated_expenses - calculated_totals['expenses']) < 0.01
    )

    return {
        "success": True,
        "valid": is_valid,
        "calculated": calculated_totals,
        "stated": {
            "income": stated_income,
            "expenses": stated_expenses,
            "net": stated_income - stated_expenses
        }
    }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Accounting Manager')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Log transaction
    log_parser = subparsers.add_parser('log', help='Log a transaction')
    log_parser.add_argument('--type', required=True, choices=['income', 'expense'], help='Transaction type')
    log_parser.add_argument('--amount', required=True, type=float, help='Transaction amount')
    log_parser.add_argument('--description', required=True, help='Transaction description')

    # Generate summary
    summary_parser = subparsers.add_parser('summary', help='Generate summary')
    summary_parser.add_argument('--period', choices=['week', 'month'], default='week', help='Summary period')

    # Show totals
    subparsers.add_parser('totals', help='Show current totals')

    # Validate
    subparsers.add_parser('validate', help='Validate accounting file')

    args = parser.parse_args()

    if args.command == 'log':
        result = log_transaction(args.type, args.amount, args.description)
    elif args.command == 'summary':
        result = generate_summary(args.period)
    elif args.command == 'totals':
        result = show_totals()
    elif args.command == 'validate':
        result = validate_file()
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
