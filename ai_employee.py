import os
import sys
from plan_tasks import make_plan_for_tasks

def main():
    """Main interface for the AI Employee"""
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:]).lower()
        if "make a plan for tasks" in command or "make a plan" in command:
            make_plan_for_tasks()
        elif "process tasks" in command:
            from process_tasks import process_tasks
            process_tasks()
        else:
            print(f"Command '{command}' not recognized.")
            print("Available commands: 'Make a plan for tasks', 'Process tasks'")
    else:
        print("AI Employee system ready.")
        print("Use: python ai_employee.py 'Make a plan for tasks' to analyze pending tasks")
        print("Use: python ai_employee.py 'Process tasks' to process all pending tasks")

if __name__ == "__main__":
    main()