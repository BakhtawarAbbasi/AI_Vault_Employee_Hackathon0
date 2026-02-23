#!/usr/bin/env python3
"""
Silver Tier AI Employee - Complete System Runner

This script demonstrates the full Silver Tier functionality:
1. Multiple watchers monitoring different sources
2. Reasoning workflows creating plan files
3. MCP-replacement skills for external actions
4. Human-in-the-loop approval system
5. Scheduling for recurring tasks
"""

import os
import sys
import subprocess
import threading
import time
import json


def run_scheduler():
    """Run the task scheduler in a separate thread"""
    try:
        subprocess.run([sys.executable, "scripts/scheduler.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Scheduler error: {e}")


def run_comprehensive_watcher():
    """Run the comprehensive file watcher"""
    try:
        subprocess.run([sys.executable, "scripts/watcher_comprehensive.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Comprehensive watcher error: {e}")


def run_linkedin_watcher():
    """Run the LinkedIn watcher"""
    try:
        subprocess.run([sys.executable, "scripts/watcher_linkedin.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"LinkedIn watcher error: {e}")


def demonstrate_reasoning_workflow():
    """Demonstrate the reasoning workflow by creating a sample task"""
    # Create sample task in inbox
    vault_path = "AI_Employee_Vault"
    inbox_path = os.path.join(vault_path, "Inbox")
    os.makedirs(inbox_path, exist_ok=True)

    sample_task = """# Sample Business Task

## Description
Post an update on LinkedIn about our new product launch to generate interest and sales.

## Details
- Product: New AI Employee System
- Key benefits: Automates business tasks, increases efficiency
- Target audience: Business owners and managers

## Checklist
- [ ] Create LinkedIn post content
- [ ] Schedule for optimal timing
- [ ] Monitor engagement
- [ ] Report results
"""

    task_file = os.path.join(inbox_path, "sample_business_task.md")
    with open(task_file, 'w') as f:
        f.write(sample_task)

    print(json.dumps({"info": "Created sample business task in inbox"}))

    # Process it through the reasoning workflow
    try:
        result = subprocess.run([sys.executable, "scripts/create_task_plan.py"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(json.dumps({"info": "Reasoning workflow completed", "output": result.stdout}))
        else:
            print(json.dumps({"error": f"Reasoning workflow failed: {result.stderr}"}))
    except Exception as e:
        print(json.dumps({"error": f"Error running reasoning workflow: {str(e)}"}))


def demonstrate_skills():
    """Demonstrate the MCP-replacement skills"""
    print(json.dumps({"info": "Demonstrating MCP-replacement skills:"}))

    # This would normally call the actual skills, but for demo purposes:
    skills_demo = {
        "gmail-send": "Ready to send emails via SMTP",
        "linkedin-post": "Ready to create LinkedIn posts via browser automation",
        "vault-file-manager": "Ready to move files between vault folders",
        "human-approval": "Ready to request and wait for human approvals"
    }

    print(json.dumps(skills_demo))


def main():
    """Main function to run the Silver Tier system"""
    print(json.dumps({"info": "Starting Silver Tier AI Employee System"}))

    # Create necessary vault directories
    for folder in ["Inbox", "Needs_Action", "Done", "Needs_Approval"]:
        os.makedirs(f"AI_Employee_Vault/{folder}", exist_ok=True)

    # Demonstrate the system components
    print(json.dumps({"info": "=== SILVER TIER SYSTEM COMPONENTS ==="}))

    # 1. Demonstrate reasoning workflow
    print(json.dumps({"info": "1. Demonstrating reasoning workflow..."}))
    demonstrate_reasoning_workflow()

    # 2. Demonstrate skills
    print(json.dumps({"info": "2. Demonstrating MCP-replacement skills..."}))
    demonstrate_skills()

    # 3. Show available watchers
    print(json.dumps({"info": "3. Available watchers ready to run:"}))
    watchers = {
        "comprehensive_watcher": "Monitors file system (Inbox)",
        "linkedin_watcher": "Monitors LinkedIn for business opportunities",
        "scheduler": "Runs scheduled tasks"
    }
    print(json.dumps(watchers))

    print(json.dumps({
        "info": "Silver Tier system components ready.",
        "next_steps": [
            "Run scripts/watcher_comprehensive.py for file monitoring",
            "Run scripts/watcher_linkedin.py for LinkedIn monitoring",
            "Run scripts/scheduler.py for scheduled tasks",
            "Add tasks to AI_Employee_Vault/Inbox/ to trigger workflows"
        ]
    }))


if __name__ == "__main__":
    main()