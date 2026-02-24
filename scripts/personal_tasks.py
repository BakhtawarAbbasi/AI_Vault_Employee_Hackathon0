#!/usr/bin/env python3
"""
Personal Task Handler
Manages personal tasks separate from business tasks
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
import shutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PersonalTaskHandler:
    """Handle personal tasks and workflow"""

    def __init__(self):
        """Initialize personal task handler"""
        self.base_dir = Path(__file__).parent.parent / 'AI_Employee_Vault' / 'Personal'
        self.inbox_dir = self.base_dir / 'Inbox'
        self.needs_action_dir = self.base_dir / 'Needs_Action'
        self.done_dir = self.base_dir / 'Done'
        self.notes_dir = self.base_dir / 'Notes'

        # Ensure directories exist
        for directory in [self.inbox_dir, self.needs_action_dir, self.done_dir, self.notes_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def process_inbox(self) -> dict:
        """
        Process personal inbox tasks

        Returns:
            Dict with processing results
        """
        try:
            inbox_files = list(self.inbox_dir.glob('*.md'))

            if not inbox_files:
                return {
                    "success": True,
                    "message": "No personal tasks in inbox",
                    "processed": 0
                }

            processed = 0
            for task_file in inbox_files:
                # Read task
                with open(task_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if task needs action
                if self._needs_action(content):
                    # Move to Needs_Action
                    dest = self.needs_action_dir / task_file.name
                    shutil.move(str(task_file), str(dest))
                    logger.info(f"Moved to Needs_Action: {task_file.name}")
                else:
                    # Move to Done
                    dest = self.done_dir / task_file.name
                    shutil.move(str(task_file), str(dest))
                    logger.info(f"Moved to Done: {task_file.name}")

                processed += 1

            # Log activity
            self._log_business_activity(f"Processed {processed} personal tasks from inbox")

            return {
                "success": True,
                "message": f"Processed {processed} personal tasks",
                "processed": processed
            }

        except Exception as e:
            error_msg = f"Failed to process personal inbox: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def create_task(self, title: str, description: str, priority: str = 'medium') -> dict:
        """
        Create a new personal task

        Args:
            title: Task title
            description: Task description
            priority: Task priority (low, medium, high)

        Returns:
            Dict with success status and task details
        """
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]
            filename = f"{timestamp}_{safe_title}.md"

            # Create task content
            task_content = f"""# {title}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Priority:** {priority}
**Status:** Pending

## Description

{description}

## Notes

(Add notes here)

## Completion

- [ ] Task completed
"""

            # Write to inbox
            task_file = self.inbox_dir / filename
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(task_content)

            # Log activity
            self._log_business_activity(f"Created personal task: {title}")

            logger.info(f"Created personal task: {filename}")

            return {
                "success": True,
                "message": "Personal task created",
                "task_file": str(task_file),
                "title": title,
                "priority": priority
            }

        except Exception as e:
            error_msg = f"Failed to create personal task: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def list_tasks(self, status: str = 'all') -> dict:
        """
        List personal tasks

        Args:
            status: Filter by status (inbox, needs_action, done, all)

        Returns:
            Dict with task list
        """
        try:
            tasks = []

            if status in ['inbox', 'all']:
                inbox_tasks = self._get_tasks_from_dir(self.inbox_dir, 'inbox')
                tasks.extend(inbox_tasks)

            if status in ['needs_action', 'all']:
                action_tasks = self._get_tasks_from_dir(self.needs_action_dir, 'needs_action')
                tasks.extend(action_tasks)

            if status in ['done', 'all']:
                done_tasks = self._get_tasks_from_dir(self.done_dir, 'done')
                tasks.extend(done_tasks)

            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks)
            }

        except Exception as e:
            error_msg = f"Failed to list personal tasks: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def complete_task(self, task_file: str) -> dict:
        """
        Mark a personal task as complete

        Args:
            task_file: Path to task file

        Returns:
            Dict with success status
        """
        try:
            task_path = Path(task_file)

            if not task_path.exists():
                return {"error": f"Task file not found: {task_file}"}

            # Move to Done
            dest = self.done_dir / task_path.name
            shutil.move(str(task_path), str(dest))

            # Update completion timestamp
            with open(dest, 'r', encoding='utf-8') as f:
                content = f.read()

            completion_note = f"\n\n**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += completion_note

            with open(dest, 'w', encoding='utf-8') as f:
                f.write(content)

            # Log activity
            self._log_business_activity(f"Completed personal task: {task_path.name}")

            logger.info(f"Completed personal task: {task_path.name}")

            return {
                "success": True,
                "message": "Personal task completed",
                "task_file": str(dest)
            }

        except Exception as e:
            error_msg = f"Failed to complete personal task: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def _needs_action(self, content: str) -> bool:
        """Check if task needs action"""
        # Simple heuristic: if it has unchecked boxes or "TODO", it needs action
        return '- [ ]' in content or 'TODO' in content.upper()

    def _get_tasks_from_dir(self, directory: Path, status: str) -> list:
        """Get tasks from a directory"""
        tasks = []
        for task_file in directory.glob('*.md'):
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title (first line starting with #)
                title = "Untitled"
                for line in content.split('\n'):
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break

                tasks.append({
                    'file': str(task_file),
                    'name': task_file.name,
                    'title': title,
                    'status': status
                })

            except Exception as e:
                logger.error(f"Error reading task file {task_file}: {e}")

        return tasks

    def _log_business_activity(self, message: str):
        """Log to business log"""
        try:
            log_dir = Path(__file__).parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'business.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] PERSONAL: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log business activity: {e}")

    def _log_error(self, message: str):
        """Log error"""
        try:
            log_dir = Path(__file__).parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'error.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] PERSONAL_ERROR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python personal_tasks.py <command> [args]"
        }))
        sys.exit(1)

    command = sys.argv[1]
    handler = PersonalTaskHandler()

    if command == 'process-inbox':
        result = handler.process_inbox()

    elif command == 'create':
        if len(sys.argv) < 4:
            result = {"error": "Usage: python personal_tasks.py create <title> <description> [priority]"}
        else:
            title = sys.argv[2]
            description = sys.argv[3]
            priority = sys.argv[4] if len(sys.argv) > 4 else 'medium'
            result = handler.create_task(title, description, priority)

    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else 'all'
        result = handler.list_tasks(status)

    elif command == 'complete':
        if len(sys.argv) < 3:
            result = {"error": "Usage: python personal_tasks.py complete <task_file>"}
        else:
            task_file = sys.argv[2]
            result = handler.complete_task(task_file)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
