#!/usr/bin/env python3
"""
Ralph Wiggum Autonomous Loop
Provides continuous, multi-step task execution without human intervention
"""

import os
import sys
import json
import argparse
import time
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import re


# Configuration
VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "AI_Employee_Vault")
INBOX_PATH = os.path.join(VAULT_PATH, "Inbox")
NEEDS_ACTION_PATH = os.path.join(VAULT_PATH, "Needs_Action")
DONE_PATH = os.path.join(VAULT_PATH, "Done")
NEEDS_APPROVAL_PATH = os.path.join(VAULT_PATH, "Needs_Approval")
ERRORS_PATH = os.path.join(VAULT_PATH, "Errors")
LOGS_PATH = os.path.join(VAULT_PATH, "Logs")
STATE_FILE = os.path.join(VAULT_PATH, ".ralph_state.json")

# Environment variables
MAX_ITERATIONS = int(os.getenv('RALPH_MAX_ITERATIONS', '5'))
ITERATION_DELAY = int(os.getenv('RALPH_ITERATION_DELAY', '10'))
REQUIRE_APPROVAL = os.getenv('RALPH_REQUIRE_APPROVAL', 'true').lower() == 'true'
APPROVAL_TIMEOUT = int(os.getenv('RALPH_APPROVAL_TIMEOUT', '3600'))
VERBOSE = os.getenv('RALPH_VERBOSE', 'false').lower() == 'true'

# Risky keywords that require human approval
RISKY_KEYWORDS = [
    'delete', 'remove', 'drop', 'truncate', 'destroy',
    'payment', 'transfer', 'send money', 'pay', 'charge',
    'publish', 'post', 'tweet', 'share', 'broadcast',
    'cancel', 'refund', 'void'
]


def ensure_directories():
    """Ensure all required directories exist"""
    for path in [INBOX_PATH, NEEDS_ACTION_PATH, DONE_PATH, NEEDS_APPROVAL_PATH, ERRORS_PATH, LOGS_PATH]:
        os.makedirs(path, exist_ok=True)


def log_to_business_log(message):
    """Log to business.log"""
    try:
        business_log = os.path.join(LOGS_PATH, "business.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] RALPH: {message}\n"

        with open(business_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass


def get_loop_state():
    """Load loop state from file"""
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_loop_state(state):
    """Save loop state to file"""
    ensure_directories()

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, indent=2, fp=f)


def is_risky(task_content):
    """Check if task contains risky operations"""
    content_lower = task_content.lower()
    return any(keyword in content_lower for keyword in RISKY_KEYWORDS)


def analyze_task(task_file):
    """Analyze task and determine complexity"""
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title = "Untitled Task"
    for line in content.split('\n'):
        if line.strip().startswith('# '):
            title = line.strip()[2:]
            break

    # Count steps (lines starting with numbers or checkboxes)
    steps = []
    for line in content.split('\n'):
        if re.match(r'^\d+\.|\-\s*\[', line.strip()):
            steps.append(line.strip())

    # Determine if risky
    risky = is_risky(content)

    # Estimate iterations needed
    estimated_iterations = min(len(steps) + 1, MAX_ITERATIONS) if steps else 2

    return {
        'title': title,
        'content': content,
        'steps': steps,
        'complexity': 'high' if len(steps) > 3 else 'medium' if len(steps) > 1 else 'low',
        'risky': risky,
        'estimated_iterations': estimated_iterations
    }


def create_plan(task_file, analysis):
    """Create execution plan for task"""
    task_id = os.path.basename(task_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_filename = f"Plan_{timestamp}_{task_id}"
    plan_filepath = os.path.join(NEEDS_ACTION_PATH, plan_filename)

    # Generate steps from analysis
    if analysis['steps']:
        steps_section = "\n".join([
            f"### Step {i+1}: {step}\n- [ ] Status: pending\n- Action: Execute step\n- Validation: Check result\n"
            for i, step in enumerate(analysis['steps'])
        ])
    else:
        steps_section = """### Step 1: Analyze and Execute
- [ ] Status: pending
- Action: Complete task objective
- Validation: Task completed successfully
"""

    plan_content = f"""---
task_id: {task_id}
original_location: {task_file}
created: {datetime.now().isoformat()}
max_iterations: {MAX_ITERATIONS}
current_iteration: 0
status: pending
risky: {str(analysis['risky']).lower()}
---

# Task Plan: {analysis['title']}

## Objective
{analysis['title']}

## Steps

{steps_section}

## Iteration Log

---
*Created by Ralph Wiggum Autonomous Loop*
"""

    with open(plan_filepath, 'w', encoding='utf-8') as f:
        f.write(plan_content)

    log_to_business_log(f"Created plan for task {task_id}: {plan_filename}")

    return plan_filepath


def parse_plan(plan_file):
    """Parse plan file and extract current state"""
    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata
    metadata = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

    # Count completed steps
    completed_steps = content.count('- [x]')
    total_steps = content.count('- [ ]') + completed_steps

    return {
        'metadata': metadata,
        'content': content,
        'completed_steps': completed_steps,
        'total_steps': total_steps,
        'all_steps_done': completed_steps == total_steps and total_steps > 0
    }


def execute_iteration(task_file, plan_file, iteration):
    """Execute one iteration of the task"""
    log_to_business_log(f"Executing iteration {iteration} for {os.path.basename(task_file)}")

    # Parse plan
    plan = parse_plan(plan_file)

    # Check if already complete
    if plan['all_steps_done']:
        return {
            'success': True,
            'status': 'completed',
            'message': 'All steps completed'
        }

    # Simulate step execution (in real implementation, this would call actual task execution)
    # For now, we'll mark the first uncompleted step as done

    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find first uncompleted step and mark as done
    updated_content = content.replace('- [ ] Status: pending', '- [x] Status: completed', 1)

    # Add iteration log entry
    iteration_log = f"""
### Iteration {iteration} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
- Executed: Step {iteration}
- Result: Success
- Next: {"Complete" if iteration >= plan['total_steps'] else f"Step {iteration + 1}"}
"""

    # Insert before the final separator
    if '---\n*Created by Ralph Wiggum' in updated_content:
        updated_content = updated_content.replace(
            '---\n*Created by Ralph Wiggum',
            f'{iteration_log}\n---\n*Created by Ralph Wiggum'
        )

    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    # Check if task is complete
    updated_plan = parse_plan(plan_file)

    if updated_plan['all_steps_done']:
        return {
            'success': True,
            'status': 'completed',
            'message': f'Task completed in {iteration} iterations'
        }

    return {
        'success': True,
        'status': 'in_progress',
        'message': f'Iteration {iteration} completed, continuing...'
    }


def move_to_done(task_file, plan_file):
    """Move completed task to Done folder"""
    task_filename = os.path.basename(task_file)
    done_filepath = os.path.join(DONE_PATH, task_filename)

    # Move task file
    if os.path.exists(task_file):
        shutil.move(task_file, done_filepath)

    # Move plan file
    if os.path.exists(plan_file):
        plan_filename = os.path.basename(plan_file)
        done_plan_filepath = os.path.join(DONE_PATH, plan_filename)
        shutil.move(plan_file, done_plan_filepath)

    log_to_business_log(f"Task {task_filename} completed and moved to Done")

    return {
        'success': True,
        'task_location': done_filepath,
        'plan_location': done_plan_filepath
    }


def request_approval(task_file, reason):
    """Request human approval for risky operation"""
    task_filename = os.path.basename(task_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    approval_filename = f"APPROVAL_{timestamp}_{task_filename}"
    approval_filepath = os.path.join(NEEDS_APPROVAL_PATH, approval_filename)

    with open(task_file, 'r', encoding='utf-8') as f:
        task_content = f.read()

    approval_content = f"""---
type: ralph_wiggum_approval
task_file: {task_file}
reason: {reason}
requested: {datetime.now().isoformat()}
status: pending
---

# Approval Required: {task_filename}

## Reason
{reason}

## Original Task
```
{task_content}
```

## Actions
- To approve: Move this file to a file named APPROVED_{approval_filename}
- To reject: Move this file to a file named REJECTED_{approval_filename}

---
*Approval requested by Ralph Wiggum Autonomous Loop*
"""

    with open(approval_filepath, 'w', encoding='utf-8') as f:
        f.write(approval_content)

    log_to_business_log(f"Approval requested for task {task_filename}: {reason}")

    return approval_filepath


def check_approval(approval_file):
    """Check if approval has been granted"""
    approval_filename = os.path.basename(approval_file)

    # Check for approved file
    approved_file = os.path.join(NEEDS_APPROVAL_PATH, f"APPROVED_{approval_filename}")
    if os.path.exists(approved_file):
        return 'approved'

    # Check for rejected file
    rejected_file = os.path.join(NEEDS_APPROVAL_PATH, f"REJECTED_{approval_filename}")
    if os.path.exists(rejected_file):
        return 'rejected'

    return 'pending'


def process_task(task_file):
    """Process a single task through the Ralph Wiggum loop"""
    ensure_directories()

    task_id = os.path.basename(task_file)

    # Load loop state
    loop_state = get_loop_state()

    # Initialize task state if not exists
    if task_id not in loop_state:
        # Analyze task
        analysis = analyze_task(task_file)

        # Check if risky and requires approval
        if REQUIRE_APPROVAL and analysis['risky']:
            approval_file = request_approval(task_file, "Task contains risky operations")

            loop_state[task_id] = {
                'status': 'awaiting_approval',
                'approval_file': approval_file,
                'started_at': datetime.now().isoformat(),
                'current_iteration': 0
            }
            save_loop_state(loop_state)

            return {
                'success': True,
                'status': 'awaiting_approval',
                'message': 'Approval required for risky operation',
                'approval_file': approval_file
            }

        # Create plan
        plan_file = create_plan(task_file, analysis)

        loop_state[task_id] = {
            'status': 'in_progress',
            'plan_file': plan_file,
            'started_at': datetime.now().isoformat(),
            'current_iteration': 0,
            'max_iterations': MAX_ITERATIONS,
            'risky': analysis['risky']
        }
        save_loop_state(loop_state)

    task_state = loop_state[task_id]

    # Check if awaiting approval
    if task_state['status'] == 'awaiting_approval':
        approval_status = check_approval(task_state['approval_file'])

        if approval_status == 'approved':
            # Create plan and continue
            analysis = analyze_task(task_file)
            plan_file = create_plan(task_file, analysis)

            task_state['status'] = 'in_progress'
            task_state['plan_file'] = plan_file
            save_loop_state(loop_state)

        elif approval_status == 'rejected':
            # Move to errors
            task_state['status'] = 'rejected'
            save_loop_state(loop_state)

            return {
                'success': False,
                'status': 'rejected',
                'message': 'Task rejected by human'
            }
        else:
            # Still waiting
            return {
                'success': True,
                'status': 'awaiting_approval',
                'message': 'Waiting for human approval'
            }

    # Check max iterations
    if task_state['current_iteration'] >= MAX_ITERATIONS:
        log_to_business_log(f"Task {task_id} exceeded max iterations ({MAX_ITERATIONS})")

        return {
            'success': False,
            'status': 'max_iterations_exceeded',
            'message': f'Task exceeded maximum iterations ({MAX_ITERATIONS})'
        }

    # Execute iteration
    task_state['current_iteration'] += 1
    task_state['last_iteration'] = datetime.now().isoformat()
    save_loop_state(loop_state)

    result = execute_iteration(task_file, task_state['plan_file'], task_state['current_iteration'])

    # Check if completed
    if result['status'] == 'completed':
        move_to_done(task_file, task_state['plan_file'])

        task_state['status'] = 'completed'
        task_state['completed_at'] = datetime.now().isoformat()
        save_loop_state(loop_state)

        return {
            'success': True,
            'status': 'completed',
            'message': f"Task completed in {task_state['current_iteration']} iterations",
            'iterations': task_state['current_iteration']
        }

    # Continue processing
    return {
        'success': True,
        'status': 'in_progress',
        'message': f"Iteration {task_state['current_iteration']}/{MAX_ITERATIONS} completed",
        'iteration': task_state['current_iteration']
    }


def process_all_tasks():
    """Process all tasks in Inbox"""
    ensure_directories()

    if not os.path.exists(INBOX_PATH):
        return {
            'success': True,
            'tasks_processed': 0,
            'message': 'No Inbox folder found'
        }

    tasks = [f for f in os.listdir(INBOX_PATH) if f.endswith('.md')]

    if not tasks:
        return {
            'success': True,
            'tasks_processed': 0,
            'message': 'No tasks in Inbox'
        }

    results = []
    for task_filename in tasks:
        task_file = os.path.join(INBOX_PATH, task_filename)
        result = process_task(task_file)
        results.append({
            'task': task_filename,
            'result': result
        })

        # Delay between iterations
        if result['status'] == 'in_progress':
            time.sleep(ITERATION_DELAY)

    return {
        'success': True,
        'tasks_processed': len(results),
        'results': results
    }


def get_status():
    """Get status of all active loops"""
    loop_state = get_loop_state()

    active_tasks = []
    for task_id, state in loop_state.items():
        if state['status'] in ['in_progress', 'awaiting_approval']:
            started = datetime.fromisoformat(state['started_at'])
            elapsed = datetime.now() - started

            active_tasks.append({
                'task_id': task_id,
                'status': state['status'],
                'iteration': f"{state.get('current_iteration', 0)}/{state.get('max_iterations', MAX_ITERATIONS)}",
                'started': f"{int(elapsed.total_seconds() / 60)} minutes ago",
                'risky': state.get('risky', False)
            })

    return {
        'success': True,
        'active_loops': len(active_tasks),
        'tasks': active_tasks
    }


def stop_task(task_id):
    """Stop processing a specific task"""
    loop_state = get_loop_state()

    if task_id not in loop_state:
        return {
            'success': False,
            'error': f'Task {task_id} not found in loop state'
        }

    loop_state[task_id]['status'] = 'stopped'
    loop_state[task_id]['stopped_at'] = datetime.now().isoformat()
    save_loop_state(loop_state)

    log_to_business_log(f"Stopped Ralph Wiggum loop for task {task_id}")

    return {
        'success': True,
        'message': f'Stopped processing task {task_id}'
    }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Ralph Wiggum Autonomous Loop')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Process specific task
    process_parser = subparsers.add_parser('process', help='Process specific task')
    process_parser.add_argument('--task-file', required=True, help='Path to task file')

    # Process all tasks
    subparsers.add_parser('process-all', help='Process all tasks in Inbox')

    # Get status
    subparsers.add_parser('status', help='Get status of active loops')

    # Stop task
    stop_parser = subparsers.add_parser('stop', help='Stop processing task')
    stop_parser.add_argument('--task-id', required=True, help='Task ID to stop')

    args = parser.parse_args()

    if args.command == 'process':
        result = process_task(args.task_file)
    elif args.command == 'process-all':
        result = process_all_tasks()
    elif args.command == 'status':
        result = get_status()
    elif args.command == 'stop':
        result = stop_task(args.task_id)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
