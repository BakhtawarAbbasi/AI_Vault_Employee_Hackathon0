#!/usr/bin/env python3
"""
Task Scheduler for AI Employee
Implements basic scheduling functionality for recurring tasks.
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
import threading


class TaskScheduler:
    def __init__(self):
        self.scheduled_tasks = []
        self.running = False

    def add_task(self, name, interval_seconds, command, args=None):
        """Add a task to be scheduled"""
        task = {
            'name': name,
            'interval': interval_seconds,
            'command': command,
            'args': args or [],
            'last_run': None
        }
        self.scheduled_tasks.append(task)

    def run_task(self, task):
        """Execute a scheduled task"""
        try:
            cmd = [sys.executable, task['command']] + task['args']
            result = subprocess.run(cmd, capture_output=True, text=True)

            task['last_run'] = datetime.now().isoformat()

            if result.returncode == 0:
                print(json.dumps({
                    "task": task['name'],
                    "status": "completed",
                    "timestamp": task['last_run'],
                    "output": result.stdout
                }))
            else:
                print(json.dumps({
                    "task": task['name'],
                    "status": "error",
                    "timestamp": task['last_run'],
                    "error": result.stderr
                }))

        except Exception as e:
            print(json.dumps({
                "task": task['name'],
                "status": "exception",
                "error": str(e)
            }))

    def run(self):
        """Run the scheduler loop"""
        self.running = True
        print(json.dumps({"info": "Scheduler started"}))

        while self.running:
            current_time = time.time()

            for task in self.scheduled_tasks:
                # Check if it's time to run this task
                if task['last_run'] is None:
                    # Run immediately if never run before
                    self.run_task(task)
                else:
                    last_run = datetime.fromisoformat(task['last_run']).timestamp()
                    if current_time - last_run >= task['interval']:
                        self.run_task(task)

            time.sleep(1)  # Check every second

    def stop(self):
        """Stop the scheduler"""
        self.running = False


def main():
    """Main function to set up and run the scheduler"""
    scheduler = TaskScheduler()

    # Example scheduled tasks
    # Task 1: Check LinkedIn every 10 minutes
    scheduler.add_task(
        name="linkedin_monitor",
        interval_seconds=600,  # 10 minutes
        command="scripts/watcher_linkedin.py"
    )

    # Task 2: Process Inbox tasks every 5 minutes
    scheduler.add_task(
        name="process_inbox",
        interval_seconds=300,  # 5 minutes
        command="scripts/create_task_plan.py"
    )

    # Task 3: Generate CEO briefing every Sunday at 8 PM (weekly)
    # Check every hour if it's Sunday 8 PM
    scheduler.add_task(
        name="ceo_briefing",
        interval_seconds=3600,  # Check every hour
        command="scripts/ceo_briefing.py",
        args=["generate"]
    )

    # Task 4: Generate weekly accounting summary every Sunday
    scheduler.add_task(
        name="weekly_accounting_summary",
        interval_seconds=604800,  # 7 days (weekly)
        command="scripts/accounting_manager.py",
        args=["summary", "--period", "week"]
    )

    # Task 5: Check for pending error retries every minute
    scheduler.add_task(
        name="error_recovery_check",
        interval_seconds=60,  # 1 minute
        command="scripts/error_recovery.py",
        args=["check-retries"]
    )

    try:
        scheduler.run()
    except KeyboardInterrupt:
        print(json.dumps({"info": "Scheduler stopped by user"}))
        scheduler.stop()


if __name__ == "__main__":
    main()