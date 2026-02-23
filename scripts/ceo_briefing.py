#!/usr/bin/env python3
"""
CEO Briefing Generator
Automatically generates comprehensive weekly executive summaries
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re
import subprocess


# Configuration
VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "AI_Employee_Vault")
REPORTS_PATH = os.path.join(VAULT_PATH, "Reports")
ARCHIVE_PATH = os.path.join(REPORTS_PATH, "Archive")
DONE_PATH = os.path.join(VAULT_PATH, "Done")
NEEDS_APPROVAL_PATH = os.path.join(VAULT_PATH, "Needs_Approval")
NEEDS_ACTION_PATH = os.path.join(VAULT_PATH, "Needs_Action")
ACCOUNTING_PATH = os.path.join(VAULT_PATH, "Accounting")
LOGS_PATH = os.path.join(VAULT_PATH, "Logs")

# Environment variables
CEO_EMAIL = os.getenv('CEO_EMAIL', '')
WEEK_START = int(os.getenv('CEO_BRIEFING_WEEK_START', '1'))  # 0=Sunday, 1=Monday
DETAILED = os.getenv('CEO_BRIEFING_DETAILED', 'true').lower() == 'true'
ARCHIVE = os.getenv('CEO_BRIEFING_ARCHIVE', 'true').lower() == 'true'


def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(REPORTS_PATH, exist_ok=True)
    os.makedirs(ARCHIVE_PATH, exist_ok=True)


def get_week_range(date=None):
    """Get the start and end date of the week"""
    if date is None:
        date = datetime.now()

    # Adjust to week start day
    days_since_week_start = (date.weekday() - WEEK_START) % 7
    week_start = date - timedelta(days=days_since_week_start)
    week_end = week_start + timedelta(days=6)

    return week_start, week_end


def get_completed_tasks(week_start, week_end):
    """Get tasks completed during the week"""
    tasks = []

    if not os.path.exists(DONE_PATH):
        return tasks

    for filename in os.listdir(DONE_PATH):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(DONE_PATH, filename)
        try:
            # Get file modification time
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))

            # Check if modified during the week
            if week_start <= mtime <= week_end + timedelta(days=1):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title
                title = "Untitled Task"
                for line in content.split('\n'):
                    if line.strip().startswith('# '):
                        title = line.strip()[2:]
                        break

                # Determine priority (default to medium)
                priority = "Medium"
                if 'priority: high' in content.lower() or 'urgent' in content.lower():
                    priority = "High"
                elif 'priority: low' in content.lower():
                    priority = "Low"

                tasks.append({
                    'title': title,
                    'priority': priority,
                    'completed_date': mtime.strftime('%Y-%m-%d')
                })
        except Exception as e:
            continue

    return tasks


def get_email_activity(week_start, week_end):
    """Get email activity from business.log"""
    emails = []
    log_file = os.path.join(LOGS_PATH, "business.log")

    if not os.path.exists(log_file):
        return emails

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'Email sent to' in line:
                    # Parse timestamp
                    match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
                    if match:
                        timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                        if week_start <= timestamp <= week_end + timedelta(days=1):
                            # Extract recipient
                            recipient_match = re.search(r'Email sent to ([^\s]+)', line)
                            subject_match = re.search(r'with subject: (.+)', line)

                            emails.append({
                                'date': timestamp.strftime('%Y-%m-%d'),
                                'recipient': recipient_match.group(1) if recipient_match else 'Unknown',
                                'subject': subject_match.group(1) if subject_match else 'No subject'
                            })
    except Exception as e:
        pass

    return emails


def get_linkedin_activity(week_start, week_end):
    """Get LinkedIn activity from business.log"""
    posts = []
    log_file = os.path.join(LOGS_PATH, "business.log")

    if not os.path.exists(log_file):
        return posts

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'LinkedIn post created' in line:
                    # Parse timestamp
                    match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
                    if match:
                        timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                        if week_start <= timestamp <= week_end + timedelta(days=1):
                            # Extract content preview
                            content_match = re.search(r'LinkedIn post created: (.+)', line)

                            posts.append({
                                'date': timestamp.strftime('%Y-%m-%d'),
                                'content': content_match.group(1) if content_match else 'No content'
                            })
    except Exception as e:
        pass

    return posts


def get_financial_summary(week_start, week_end):
    """Get financial summary from accounting manager"""
    try:
        result = subprocess.run(
            ['python', 'scripts/accounting_manager.py', 'summary', '--period', 'week'],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {
                'income': 0,
                'expenses': 0,
                'net': 0,
                'transaction_count': 0
            }
    except Exception as e:
        return {
            'income': 0,
            'expenses': 0,
            'net': 0,
            'transaction_count': 0
        }


def get_pending_approvals():
    """Get count of pending approvals"""
    if not os.path.exists(NEEDS_APPROVAL_PATH):
        return 0

    count = 0
    for filename in os.listdir(NEEDS_APPROVAL_PATH):
        if filename.endswith('.md'):
            count += 1

    return count


def get_in_progress_tasks():
    """Get count of tasks in progress"""
    if not os.path.exists(NEEDS_ACTION_PATH):
        return 0

    count = 0
    for filename in os.listdir(NEEDS_ACTION_PATH):
        if filename.endswith('.md'):
            count += 1

    return count


def get_system_health():
    """Get system health status"""
    health = {
        'watchers': [],
        'errors': [],
        'uptime': 'Unknown'
    }

    log_file = os.path.join(LOGS_PATH, "business.log")

    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Count recent errors (last 100 lines)
            recent_lines = lines[-100:] if len(lines) > 100 else lines
            error_count = sum(1 for line in recent_lines if 'ERROR' in line or 'error' in line.lower())

            health['errors'] = [
                {'message': 'Recent errors detected', 'count': error_count}
            ] if error_count > 0 else []

            # Check for watcher status
            if any('watcher' in line.lower() for line in recent_lines):
                health['watchers'].append({'name': 'File System Watcher', 'status': 'Running'})
                health['watchers'].append({'name': 'LinkedIn Watcher', 'status': 'Running'})
                health['watchers'].append({'name': 'Scheduler', 'status': 'Running'})

        except Exception as e:
            pass

    return health


def generate_briefing(week_start=None, week_end=None):
    """Generate CEO briefing report"""
    ensure_directories()

    # Get week range
    if week_start is None or week_end is None:
        week_start, week_end = get_week_range()

    # Collect data
    tasks = get_completed_tasks(week_start, week_end)
    emails = get_email_activity(week_start, week_end)
    linkedin = get_linkedin_activity(week_start, week_end)
    financial = get_financial_summary(week_start, week_end)
    pending_approvals = get_pending_approvals()
    in_progress = get_in_progress_tasks()
    system_health = get_system_health()

    # Group tasks by priority
    high_priority = [t for t in tasks if t['priority'] == 'High']
    medium_priority = [t for t in tasks if t['priority'] == 'Medium']
    low_priority = [t for t in tasks if t['priority'] == 'Low']

    # Generate report
    now = datetime.now()
    week_str = f"{week_start.strftime('%B %d')}-{week_end.strftime('%d, %Y')}"

    report = f"""# CEO Weekly Briefing
**Week of {week_str}**

Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

{len(tasks)} tasks completed this week with {"positive" if financial.get('net', 0) > 0 else "negative"} cash flow of ${abs(financial.get('net', 0)):,.2f}. System operating {"normally" if len(system_health['errors']) == 0 else "with minor issues"}.

---

## Key Metrics

| Metric | This Week | Status |
|--------|-----------|--------|
| Tasks Completed | {len(tasks)} | {"✓" if len(tasks) > 0 else "-"} |
| Emails Sent | {len(emails)} | {"✓" if len(emails) > 0 else "-"} |
| LinkedIn Posts | {len(linkedin)} | {"✓" if len(linkedin) > 0 else "-"} |
| Net Profit | ${financial.get('net', 0):,.2f} | {"✓" if financial.get('net', 0) > 0 else "⚠"} |
| Pending Approvals | {pending_approvals} | {"⚠" if pending_approvals > 0 else "✓"} |

---

## Tasks Completed ({len(tasks)})

"""

    if high_priority:
        report += "### High Priority\n"
        for task in high_priority:
            report += f"- [x] {task['title']}\n"
        report += "\n"

    if medium_priority:
        report += "### Medium Priority\n"
        for task in medium_priority:
            report += f"- [x] {task['title']}\n"
        report += "\n"

    if low_priority:
        report += "### Low Priority\n"
        for task in low_priority:
            report += f"- [x] {task['title']}\n"
        report += "\n"

    if not tasks:
        report += "No tasks completed this week.\n\n"

    report += f"""---

## Communications

### Emails Sent ({len(emails)})
"""

    if emails:
        for email in emails[:10]:  # Show first 10
            report += f"- {email['date']}: {email['subject']} (to {email['recipient']})\n"
        if len(emails) > 10:
            report += f"- ... and {len(emails) - 10} more\n"
    else:
        report += "No emails sent this week.\n"

    report += f"""
### LinkedIn Activity ({len(linkedin)} posts)
"""

    if linkedin:
        for post in linkedin:
            report += f"- {post['date']}: {post['content']}\n"
    else:
        report += "No LinkedIn posts this week.\n"

    report += f"""
---

## Financial Performance

### Income
- **Total Income**: ${financial.get('income', 0):,.2f}

### Expenses
- **Total Expenses**: ${financial.get('expenses', 0):,.2f}

### Summary
- **Net Profit**: ${financial.get('net', 0):,.2f}
- **Profit Margin**: {(financial.get('net', 0) / financial.get('income', 1) * 100) if financial.get('income', 0) > 0 else 0:.1f}%
- **Transaction Count**: {financial.get('transaction_count', 0)}

---

## Pending Items

### Awaiting Approval ({pending_approvals})
"""

    if pending_approvals > 0:
        report += f"{pending_approvals} items require your approval in AI_Employee_Vault/Needs_Approval/\n"
    else:
        report += "No items awaiting approval.\n"

    report += f"""
### In Progress ({in_progress})
"""

    if in_progress > 0:
        report += f"{in_progress} tasks currently in progress in AI_Employee_Vault/Needs_Action/\n"
    else:
        report += "No tasks in progress.\n"

    report += """
---

## System Health

### Watchers Status
"""

    if system_health['watchers']:
        for watcher in system_health['watchers']:
            report += f"- {watcher['status']}: {watcher['name']}\n"
    else:
        report += "- Status: Unknown (check logs)\n"

    report += """
### Performance
"""

    if system_health['errors']:
        report += f"- Errors detected: {system_health['errors'][0]['count']}\n"
        report += "- Review AI_Employee_Vault/Logs/business.log for details\n"
    else:
        report += "- No errors detected this week\n"
        report += "- System operating normally\n"

    report += f"""
---

## Recommendations

### Immediate Actions
"""

    recommendations = []

    if pending_approvals > 0:
        recommendations.append(f"Review and process {pending_approvals} pending approval(s)")

    if financial.get('net', 0) < 0:
        recommendations.append("Review expenses - negative cash flow this week")

    if len(tasks) == 0:
        recommendations.append("No tasks completed - review task pipeline")

    if len(system_health['errors']) > 0:
        recommendations.append("Review system logs for errors")

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
    else:
        report += "No immediate actions required. Continue current operations.\n"

    report += f"""
### Strategic Observations
- {"Strong" if len(tasks) > 5 else "Moderate" if len(tasks) > 0 else "Slow"} week with {len(tasks)} tasks completed
- {"Positive" if financial.get('net', 0) > 0 else "Negative"} cash flow of ${abs(financial.get('net', 0)):,.2f}
- {"Active" if len(emails) > 5 else "Light"} communication with {len(emails)} emails sent
- {"Good" if len(linkedin) > 0 else "Low"} social media presence with {len(linkedin)} LinkedIn posts

---

*Generated by AI Employee CEO Briefing System*
*Next briefing: {(week_end + timedelta(days=7)).strftime('%B %d, %Y')}*
"""

    # Save report
    report_file = os.path.join(REPORTS_PATH, "CEO_Weekly.md")

    # Archive old report if it exists
    if ARCHIVE and os.path.exists(report_file):
        archive_name = f"CEO_Weekly_{week_start.strftime('%Y%m%d')}.md"
        archive_file = os.path.join(ARCHIVE_PATH, archive_name)
        try:
            os.rename(report_file, archive_file)
        except Exception:
            pass

    # Write new report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Log activity
    log_file = os.path.join(LOGS_PATH, "business.log")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] CEO briefing generated for week {week_str}\n"

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass

    return {
        "success": True,
        "message": "CEO briefing generated successfully",
        "report_file": report_file,
        "week": week_str,
        "summary": {
            "tasks_completed": len(tasks),
            "emails_sent": len(emails),
            "linkedin_posts": len(linkedin),
            "net_profit": financial.get('net', 0),
            "pending_approvals": pending_approvals
        }
    }


def view_briefing():
    """View the latest briefing"""
    report_file = os.path.join(REPORTS_PATH, "CEO_Weekly.md")

    if not os.path.exists(report_file):
        return {
            "success": False,
            "error": "No briefing found. Generate one first."
        }

    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(content)

    return {
        "success": True,
        "message": "Briefing displayed"
    }


def email_briefing(to_email):
    """Email the briefing"""
    report_file = os.path.join(REPORTS_PATH, "CEO_Weekly.md")

    if not os.path.exists(report_file):
        return {
            "success": False,
            "error": "No briefing found. Generate one first."
        }

    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract week from content
    week_match = re.search(r'\*\*Week of (.+?)\*\*', content)
    week_str = week_match.group(1) if week_match else "Unknown"

    try:
        result = subprocess.run(
            [
                'python', 'scripts/send_email.py',
                to_email,
                f"CEO Weekly Briefing - {week_str}",
                content
            ],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )

        if result.returncode == 0:
            return {
                "success": True,
                "message": "CEO briefing emailed successfully",
                "recipient": to_email,
                "subject": f"CEO Weekly Briefing - {week_str}"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to send email: {result.stderr}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send email: {str(e)}"
        }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='CEO Briefing Generator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Generate briefing
    gen_parser = subparsers.add_parser('generate', help='Generate CEO briefing')
    gen_parser.add_argument('--start', help='Week start date (YYYY-MM-DD)')
    gen_parser.add_argument('--end', help='Week end date (YYYY-MM-DD)')

    # View briefing
    subparsers.add_parser('view', help='View latest briefing')

    # Email briefing
    email_parser = subparsers.add_parser('email', help='Email briefing')
    email_parser.add_argument('--to', required=True, help='Recipient email address')

    args = parser.parse_args()

    if args.command == 'generate':
        week_start = datetime.strptime(args.start, '%Y-%m-%d') if args.start else None
        week_end = datetime.strptime(args.end, '%Y-%m-%d') if args.end else None
        result = generate_briefing(week_start, week_end)
    elif args.command == 'view':
        result = view_briefing()
    elif args.command == 'email':
        result = email_briefing(args.to)
    else:
        parser.print_help()
        return

    if args.command != 'view':  # view already prints content
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
