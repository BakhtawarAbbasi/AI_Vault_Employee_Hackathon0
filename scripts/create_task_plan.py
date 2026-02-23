#!/usr/bin/env python3
"""
Task Plan Generator
Creates detailed plan files for tasks found in vault/Inbox
"""

import os
import re
from datetime import datetime
from pathlib import Path


def read_task_file(filepath):
    """Read the content of a task file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_task_title(content):
    """Extract the title from the task content"""
    # Look for the first heading
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip()[2:]  # Remove '# ' prefix
    return "Untitled Task"


def create_plan_content(original_task_content, original_filename):
    """Create the detailed plan content based on the original task"""
    # Extract title from the original task
    task_title = extract_task_title(original_task_content)

    # Generate timestamp for the plan
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the plan content
    plan_content = f"""# Task Plan

## Original Task
```
{original_task_content.strip()}
```

## Objective
To complete the task '{task_title}' by following a structured approach that ensures all requirements are met efficiently.

## Step-by-Step Plan
1. Analyze the original task requirements in detail
2. Identify all necessary steps and resources needed
3. Determine potential challenges and solutions
4. Execute the planned steps systematically
5. Verify completion against original requirements
6. Document the results and move to Done folder

## Priority
Medium

## Requires Human Approval?
No

## Suggested Output
[Based on the original task requirements, the expected output would include all deliverables mentioned in the original task]

---
Plan created on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Original file: {original_filename}
"""
    return plan_content


def create_task_plan(task_filepath):
    """Create a detailed plan for a task and save it to Needs_Action"""
    # Read the original task
    original_content = read_task_file(task_filepath)
    original_filename = os.path.basename(task_filepath)

    # Create the plan content
    plan_content = create_plan_content(original_content, original_filename)

    # Generate filename for the plan
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_filename = f"Plan_{timestamp}.md"
    plan_filepath = os.path.join("AI_Employee_Vault", "Needs_Action", plan_filename)

    # Ensure the Needs_Action directory exists
    os.makedirs(os.path.join("AI_Employee_Vault", "Needs_Action"), exist_ok=True)

    # Write the plan to file
    with open(plan_filepath, 'w', encoding='utf-8') as f:
        f.write(plan_content)

    return plan_filepath


def main():
    """Main function to process tasks from vault/Inbox"""
    inbox_path = os.path.join("AI_Employee_Vault", "Inbox")

    # Check if Inbox directory exists
    if not os.path.exists(inbox_path):
        os.makedirs(inbox_path, exist_ok=True)
        print(f"Inbox directory created: {inbox_path}")

    # Get all .md files in the Inbox that haven't been processed yet
    task_files = []
    if os.path.exists(inbox_path):  # Only try to list if directory exists
        for filename in os.listdir(inbox_path):
            if filename.endswith('.md'):
                filepath = os.path.join(inbox_path, filename)
                if os.path.isfile(filepath):
                    task_files.append(filepath)

    if not task_files:
        print("No task files found in vault/Inbox")
        return

    # Process each task file
    created_plans = []
    for task_filepath in task_files:
        try:
            plan_filepath = create_task_plan(task_filepath)
            created_plans.append(plan_filepath)
            print(f"Created plan: {plan_filepath}")
        except Exception as e:
            print(f"Error processing {task_filepath}: {str(e)}")

    if created_plans:
        print(f"\nSuccessfully created {len(created_plans)} plan file(s):")
        for plan in created_plans:
            print(f"  - {plan}")
    else:
        print("No plans were created")


if __name__ == "__main__":
    main()