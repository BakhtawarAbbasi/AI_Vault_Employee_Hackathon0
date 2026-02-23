#!/usr/bin/env python3
"""
Error Recovery System
Handles error logging, task recovery, and automatic retry mechanisms
"""

import os
import sys
import json
import argparse
import traceback
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import time


# Configuration
VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "AI_Employee_Vault")
ERRORS_PATH = os.path.join(VAULT_PATH, "Errors")
LOGS_PATH = os.path.join(VAULT_PATH, "Logs")
ERROR_LOG = os.path.join(LOGS_PATH, "error.log")
RETRY_STATE_FILE = os.path.join(ERRORS_PATH, ".retry_state.json")

# Environment variables
RETRY_DELAY = int(os.getenv('ERROR_RETRY_DELAY', '300'))  # 5 minutes
MAX_RETRIES = int(os.getenv('ERROR_MAX_RETRIES', '3'))
EXPONENTIAL_BACKOFF = os.getenv('ERROR_EXPONENTIAL_BACKOFF', 'true').lower() == 'true'
ALERT_EMAIL = os.getenv('ERROR_ALERT_EMAIL', '')
LOG_MAX_SIZE = int(os.getenv('ERROR_LOG_MAX_SIZE', '10')) * 1024 * 1024  # MB to bytes


def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(ERRORS_PATH, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)


def rotate_log_if_needed():
    """Rotate error log if it exceeds max size"""
    if os.path.exists(ERROR_LOG) and os.path.getsize(ERROR_LOG) > LOG_MAX_SIZE:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = os.path.join(LOGS_PATH, f"error_{timestamp}.log")
        shutil.move(ERROR_LOG, archive_name)


def log_to_error_log(message):
    """Write message to error.log"""
    ensure_directories()
    rotate_log_if_needed()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    with open(ERROR_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def log_to_business_log(message):
    """Log to business.log for audit trail"""
    try:
        business_log = os.path.join(LOGS_PATH, "business.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(business_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass


def get_retry_state():
    """Load retry state from file"""
    if not os.path.exists(RETRY_STATE_FILE):
        return {}

    try:
        with open(RETRY_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_retry_state(state):
    """Save retry state to file"""
    ensure_directories()

    with open(RETRY_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, indent=2, fp=f)


def calculate_retry_delay(attempt):
    """Calculate retry delay with optional exponential backoff"""
    if EXPONENTIAL_BACKOFF:
        return RETRY_DELAY * (2 ** (attempt - 1))
    else:
        return RETRY_DELAY


def log_error(task_id, error_type, error_message, stack_trace=None, context=None, original_location=None):
    """Log an error and prepare for retry"""
    ensure_directories()

    # Log to error.log
    log_to_error_log(f"ERROR | Task: {task_id} | Type: {error_type} | Message: {error_message}")

    if stack_trace:
        log_to_error_log(f"STACK | {stack_trace}")

    if context:
        context_str = ", ".join([f"{k}: {v}" for k, v in context.items()])
        log_to_error_log(f"CONTEXT | {context_str}")

    # Log to business.log
    log_to_business_log(f"ERROR: Task {task_id} failed with {error_type}: {error_message}")

    # Load retry state
    retry_state = get_retry_state()

    # Initialize or update task retry info
    if task_id not in retry_state:
        retry_state[task_id] = {
            'retry_count': 0,
            'error_type': error_type,
            'error_message': error_message,
            'first_error': datetime.now().isoformat(),
            'original_location': original_location or 'unknown'
        }

    retry_count = retry_state[task_id]['retry_count']

    if retry_count < MAX_RETRIES:
        # Schedule retry
        retry_count += 1
        retry_delay = calculate_retry_delay(retry_count)
        next_retry = datetime.now() + timedelta(seconds=retry_delay)

        retry_state[task_id]['retry_count'] = retry_count
        retry_state[task_id]['next_retry'] = next_retry.isoformat()
        retry_state[task_id]['status'] = 'pending_retry'

        log_to_error_log(f"RETRY | Attempt {retry_count}/{MAX_RETRIES} scheduled for {next_retry.strftime('%Y-%m-%d %H:%M:%S')}")
        log_to_business_log(f"Retry scheduled for task {task_id}: attempt {retry_count}/{MAX_RETRIES}")
    else:
        # Max retries reached
        retry_state[task_id]['status'] = 'permanent_failure'
        log_to_error_log(f"PERMANENT_FAILURE | Task: {task_id} | Max retries ({MAX_RETRIES}) exceeded")
        log_to_business_log(f"PERMANENT FAILURE: Task {task_id} exceeded max retries")

        # Send alert if configured
        if ALERT_EMAIL:
            send_error_alert(task_id, error_type, error_message)

    # Save retry state
    save_retry_state(retry_state)

    log_to_error_log("---")

    return {
        'success': True,
        'task_id': task_id,
        'retry_count': retry_count,
        'max_retries': MAX_RETRIES,
        'status': retry_state[task_id]['status']
    }


def move_to_errors(task_file, error_type, error_message, stack_trace=None, context=None):
    """Move failed task to Errors folder with metadata"""
    ensure_directories()

    if not os.path.exists(task_file):
        return {
            'success': False,
            'error': f"Task file not found: {task_file}"
        }

    # Read original task content
    with open(task_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Generate error file name
    task_name = os.path.basename(task_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_filename = f"{os.path.splitext(task_name)[0]}_ERROR_{timestamp}.md"
    error_filepath = os.path.join(ERRORS_PATH, error_filename)

    # Get retry state
    retry_state = get_retry_state()
    task_id = task_name
    task_info = retry_state.get(task_id, {})

    retry_count = task_info.get('retry_count', 0)
    next_retry = task_info.get('next_retry', 'N/A')
    status = task_info.get('status', 'pending_retry')

    # Create error file with metadata
    error_content = f"""---
original_location: {task_file}
error_timestamp: {datetime.now().isoformat()}
error_type: {error_type}
error_message: {error_message}
retry_count: {retry_count}
max_retries: {MAX_RETRIES}
next_retry: {next_retry}
status: {status}
---

# Original Task Content

{original_content}

---

## Error Details

**Error Type**: {error_type}
**Error Message**: {error_message}
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    if stack_trace:
        error_content += f"""
**Stack Trace**:
```
{stack_trace}
```
"""

    if context:
        error_content += "\n**Context**:\n"
        for key, value in context.items():
            error_content += f"- {key}: {value}\n"

    error_content += f"""
## Recovery Actions

- [x] Error logged to logs/error.log
- [x] Task moved to Errors folder
- {'[ ]' if status == 'pending_retry' else '[x]'} Retry scheduled for {next_retry}
- {'[ ]' if status != 'permanent_failure' else '[x]'} Manual intervention required

---
*Error captured by Error Recovery System*
"""

    # Write error file
    with open(error_filepath, 'w', encoding='utf-8') as f:
        f.write(error_content)

    # Remove original file
    os.remove(task_file)

    log_to_business_log(f"Task {task_name} moved to Errors folder: {error_filename}")

    return {
        'success': True,
        'original_file': task_file,
        'error_file': error_filepath,
        'status': status
    }


def check_pending_retries():
    """Check for tasks that need to be retried"""
    retry_state = get_retry_state()
    now = datetime.now()
    retries_due = []

    for task_id, info in retry_state.items():
        if info.get('status') == 'pending_retry':
            next_retry_str = info.get('next_retry')
            if next_retry_str:
                next_retry = datetime.fromisoformat(next_retry_str)
                if now >= next_retry:
                    retries_due.append({
                        'task_id': task_id,
                        'retry_count': info['retry_count'],
                        'original_location': info.get('original_location', 'unknown')
                    })

    return retries_due


def retry_task(task_id):
    """Retry a failed task"""
    retry_state = get_retry_state()

    if task_id not in retry_state:
        return {
            'success': False,
            'error': f"Task {task_id} not found in retry state"
        }

    task_info = retry_state[task_id]

    # Find error file
    error_files = [f for f in os.listdir(ERRORS_PATH) if f.startswith(os.path.splitext(task_id)[0]) and f.endswith('.md')]

    if not error_files:
        return {
            'success': False,
            'error': f"Error file not found for task {task_id}"
        }

    error_file = os.path.join(ERRORS_PATH, error_files[0])

    # Read error file to get original location
    with open(error_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract original location from metadata
    import re
    location_match = re.search(r'original_location:\s*(.+)', content)
    original_location = location_match.group(1).strip() if location_match else None

    if not original_location:
        return {
            'success': False,
            'error': "Could not determine original location"
        }

    # Extract original content
    content_match = re.search(r'# Original Task Content\n\n(.+?)\n\n---', content, re.DOTALL)
    original_content = content_match.group(1).strip() if content_match else content

    # Move back to original location
    try:
        with open(original_location, 'w', encoding='utf-8') as f:
            f.write(original_content)

        # Remove error file
        os.remove(error_file)

        # Update retry state
        retry_state[task_id]['status'] = 'retrying'
        save_retry_state(retry_state)

        log_to_error_log(f"RETRY | Task: {task_id} | Attempt: {task_info['retry_count']}/{MAX_RETRIES}")
        log_to_business_log(f"Retrying task {task_id} (attempt {task_info['retry_count']}/{MAX_RETRIES})")

        return {
            'success': True,
            'task_id': task_id,
            'retry_count': task_info['retry_count'],
            'restored_to': original_location
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to retry task: {str(e)}"
        }


def check_retries():
    """Check and execute pending retries"""
    retries_due = check_pending_retries()

    results = []
    for retry_info in retries_due:
        result = retry_task(retry_info['task_id'])
        results.append(result)

    return {
        'success': True,
        'retries_executed': len(results),
        'results': results
    }


def get_error_status():
    """Get current error status"""
    retry_state = get_retry_state()

    total_errors = len(retry_state)
    pending_retry = sum(1 for info in retry_state.values() if info.get('status') == 'pending_retry')
    permanent_failures = sum(1 for info in retry_state.values() if info.get('status') == 'permanent_failure')
    resolved = sum(1 for info in retry_state.values() if info.get('status') == 'resolved')

    # Get recent errors
    recent_errors = []
    for task_id, info in list(retry_state.items())[:5]:
        recent_errors.append({
            'task': task_id,
            'error': info.get('error_type', 'Unknown'),
            'timestamp': info.get('first_error', 'Unknown'),
            'status': info.get('status', 'unknown'),
            'next_retry': info.get('next_retry', 'N/A')
        })

    return {
        'success': True,
        'total_errors': total_errors,
        'pending_retry': pending_retry,
        'permanent_failures': permanent_failures,
        'resolved': resolved,
        'recent_errors': recent_errors
    }


def generate_error_report(period='week'):
    """Generate error report for specified period"""
    # Parse error log
    if not os.path.exists(ERROR_LOG):
        return {
            'success': True,
            'period': period,
            'total_errors': 0,
            'error_rate': '0%',
            'most_common_errors': [],
            'recovery_rate': '0%',
            'permanent_failures': 0
        }

    # Calculate date range
    now = datetime.now()
    if period == 'day':
        start_date = now - timedelta(days=1)
    elif period == 'week':
        start_date = now - timedelta(days=7)
    elif period == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=7)

    # Parse error log
    error_types = {}
    total_errors = 0

    with open(ERROR_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            if 'ERROR |' in line:
                # Extract timestamp
                timestamp_match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
                if timestamp_match:
                    timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
                    if timestamp >= start_date:
                        total_errors += 1

                        # Extract error type
                        type_match = re.search(r'Type:\s*(\w+)', line)
                        if type_match:
                            error_type = type_match.group(1)
                            error_types[error_type] = error_types.get(error_type, 0) + 1

    # Get retry state
    retry_state = get_retry_state()
    permanent_failures = sum(1 for info in retry_state.values() if info.get('status') == 'permanent_failure')
    resolved = sum(1 for info in retry_state.values() if info.get('status') == 'resolved')

    # Calculate recovery rate
    recovery_rate = (resolved / total_errors * 100) if total_errors > 0 else 0

    # Sort error types by count
    most_common = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]
    most_common_errors = [{'type': t, 'count': c} for t, c in most_common]

    period_str = f"Last {period}" if period in ['day', 'week', 'month'] else period

    return {
        'success': True,
        'period': period_str,
        'total_errors': total_errors,
        'error_rate': f"{(total_errors / 100):.1f}%",  # Simplified calculation
        'most_common_errors': most_common_errors,
        'recovery_rate': f"{recovery_rate:.1f}%",
        'permanent_failures': permanent_failures
    }


def send_error_alert(task_id, error_type, error_message):
    """Send error alert email"""
    if not ALERT_EMAIL:
        return

    try:
        import subprocess
        subject = f"Critical Error: {error_type} in {task_id}"
        body = f"""Critical error detected in AI Employee system:

Task: {task_id}
Error Type: {error_type}
Error Message: {error_message}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This task has exceeded the maximum retry limit and requires manual intervention.

Please review the error details in AI_Employee_Vault/Errors/ folder.
"""

        subprocess.run(
            ['python', 'scripts/send_email.py', ALERT_EMAIL, subject, body],
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
    except Exception:
        pass


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Error Recovery System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Check status
    subparsers.add_parser('check', help='Check error status')

    # Check and execute retries
    subparsers.add_parser('check-retries', help='Check and execute pending retries')

    # Retry specific task
    retry_parser = subparsers.add_parser('retry', help='Retry specific task')
    retry_parser.add_argument('--task-id', required=True, help='Task ID to retry')

    # Retry all
    subparsers.add_parser('retry-all', help='Retry all pending tasks')

    # Generate report
    report_parser = subparsers.add_parser('report', help='Generate error report')
    report_parser.add_argument('--period', choices=['day', 'week', 'month'], default='week', help='Report period')

    args = parser.parse_args()

    if args.command == 'check':
        result = get_error_status()
    elif args.command == 'check-retries':
        result = check_retries()
    elif args.command == 'retry':
        result = retry_task(args.task_id)
    elif args.command == 'retry-all':
        result = check_retries()
    elif args.command == 'report':
        result = generate_error_report(args.period)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
