#!/usr/bin/env python3
"""
Cross-Domain Task Router
Routes tasks between Personal and Business domains
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


class CrossDomainRouter:
    """Route tasks between Personal and Business domains"""

    def __init__(self):
        """Initialize cross-domain router"""
        self.base_dir = Path(__file__).parent.parent / 'AI_Employee_Vault'

        # Business domain paths
        self.business_inbox = self.base_dir / 'Inbox'
        self.business_needs_action = self.base_dir / 'Needs_Action'
        self.business_done = self.base_dir / 'Done'

        # Personal domain paths
        self.personal_inbox = self.base_dir / 'Personal' / 'Inbox'
        self.personal_needs_action = self.base_dir / 'Personal' / 'Needs_Action'
        self.personal_done = self.base_dir / 'Personal' / 'Done'

        # Cross-domain paths
        self.cross_domain_dir = self.base_dir / 'Cross_Domain'
        self.cross_domain_dir.mkdir(exist_ok=True)

        # Keywords for domain classification
        self.personal_keywords = [
            'personal', 'home', 'family', 'health', 'grocery', 'groceries',
            'doctor', 'dentist', 'appointment', 'exercise', 'gym', 'vacation',
            'birthday', 'anniversary', 'hobby', 'friend', 'relative'
        ]

        self.business_keywords = [
            'business', 'client', 'customer', 'invoice', 'payment', 'project',
            'meeting', 'proposal', 'contract', 'revenue', 'sales', 'marketing',
            'linkedin', 'twitter', 'facebook', 'instagram', 'social media',
            'accounting', 'odoo', 'ceo', 'briefing'
        ]

    def classify_task(self, task_file: Path) -> str:
        """
        Classify task as personal, business, or cross-domain

        Args:
            task_file: Path to task file

        Returns:
            'personal', 'business', or 'cross-domain'
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            personal_score = sum(1 for kw in self.personal_keywords if kw in content)
            business_score = sum(1 for kw in self.business_keywords if kw in content)

            # If both scores are significant, it's cross-domain
            if personal_score >= 2 and business_score >= 2:
                return 'cross-domain'

            # If one score is clearly higher
            if personal_score > business_score:
                return 'personal'
            elif business_score > personal_score:
                return 'business'

            # Default to business if unclear
            return 'business'

        except Exception as e:
            logger.error(f"Error classifying task {task_file}: {e}")
            return 'business'

    def route_task(self, task_file: Path, source_domain: str = None) -> dict:
        """
        Route task to appropriate domain

        Args:
            task_file: Path to task file
            source_domain: Source domain ('personal' or 'business')

        Returns:
            Dict with routing result
        """
        try:
            classification = self.classify_task(task_file)

            # Determine destination
            if classification == 'cross-domain':
                dest_dir = self.cross_domain_dir
                domain = 'cross-domain'
            elif classification == 'personal':
                dest_dir = self.personal_inbox
                domain = 'personal'
            else:
                dest_dir = self.business_inbox
                domain = 'business'

            # Move task to destination
            dest_file = dest_dir / task_file.name
            shutil.move(str(task_file), str(dest_file))

            # Log routing
            self._log_routing(task_file.name, source_domain or 'unknown', domain)

            logger.info(f"Routed {task_file.name} to {domain} domain")

            return {
                "success": True,
                "task": task_file.name,
                "source": source_domain,
                "destination": domain,
                "classification": classification
            }

        except Exception as e:
            error_msg = f"Failed to route task: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def process_cross_domain_tasks(self) -> dict:
        """
        Process tasks in cross-domain folder

        Returns:
            Dict with processing results
        """
        try:
            cross_domain_tasks = list(self.cross_domain_dir.glob('*.md'))

            if not cross_domain_tasks:
                return {
                    "success": True,
                    "message": "No cross-domain tasks to process",
                    "processed": 0
                }

            processed = 0
            results = []

            for task_file in cross_domain_tasks:
                # Read task content
                with open(task_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Create linked tasks in both domains
                personal_task = self._create_linked_task(
                    task_file, 'personal', content
                )
                business_task = self._create_linked_task(
                    task_file, 'business', content
                )

                results.append({
                    'original': task_file.name,
                    'personal_task': personal_task,
                    'business_task': business_task
                })

                # Move original to archive
                archive_dir = self.cross_domain_dir / 'Archive'
                archive_dir.mkdir(exist_ok=True)
                shutil.move(str(task_file), str(archive_dir / task_file.name))

                processed += 1

            # Log activity
            self._log_business_activity(
                f"Processed {processed} cross-domain tasks"
            )

            return {
                "success": True,
                "message": f"Processed {processed} cross-domain tasks",
                "processed": processed,
                "results": results
            }

        except Exception as e:
            error_msg = f"Failed to process cross-domain tasks: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def _create_linked_task(self, original_task: Path, domain: str, content: str) -> str:
        """Create a linked task in specified domain"""
        try:
            # Determine destination
            if domain == 'personal':
                dest_dir = self.personal_needs_action
                other_domain = 'business'
            else:
                dest_dir = self.business_needs_action
                other_domain = 'personal'

            # Create task file with cross-reference
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            task_name = f"{timestamp}_cross_domain_{domain}_{original_task.stem}.md"
            task_file = dest_dir / task_name

            # Add cross-domain metadata
            linked_content = f"""---
type: cross-domain
original_task: {original_task.name}
domain: {domain}
linked_domain: {other_domain}
created: {datetime.now().isoformat()}
---

# Cross-Domain Task: {domain.title()}

**Note:** This task has both personal and business components.

{content}

---

## Cross-Domain Links
- Original task: {original_task.name}
- Linked {other_domain} task: Check {other_domain.title()} domain

## Completion
When completing this task, ensure the linked task in {other_domain} domain is also updated.
"""

            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(linked_content)

            return task_name

        except Exception as e:
            logger.error(f"Error creating linked task: {e}")
            return None

    def generate_unified_report(self) -> dict:
        """
        Generate unified report across both domains

        Returns:
            Dict with unified statistics
        """
        try:
            # Count tasks in each domain
            business_inbox = len(list(self.business_inbox.glob('*.md')))
            business_needs_action = len(list(self.business_needs_action.glob('*.md')))
            business_done = len(list(self.business_done.glob('*.md')))

            personal_inbox = len(list(self.personal_inbox.glob('*.md')))
            personal_needs_action = len(list(self.personal_needs_action.glob('*.md')))
            personal_done = len(list(self.personal_done.glob('*.md')))

            cross_domain = len(list(self.cross_domain_dir.glob('*.md')))

            # Calculate totals
            total_inbox = business_inbox + personal_inbox
            total_needs_action = business_needs_action + personal_needs_action
            total_done = business_done + personal_done
            total_tasks = total_inbox + total_needs_action + total_done + cross_domain

            report = {
                "success": True,
                "generated": datetime.now().isoformat(),
                "business": {
                    "inbox": business_inbox,
                    "needs_action": business_needs_action,
                    "done": business_done,
                    "total": business_inbox + business_needs_action + business_done
                },
                "personal": {
                    "inbox": personal_inbox,
                    "needs_action": personal_needs_action,
                    "done": personal_done,
                    "total": personal_inbox + personal_needs_action + personal_done
                },
                "cross_domain": cross_domain,
                "totals": {
                    "inbox": total_inbox,
                    "needs_action": total_needs_action,
                    "done": total_done,
                    "cross_domain": cross_domain,
                    "all_tasks": total_tasks
                }
            }

            # Write report to file
            report_file = self.base_dir / 'Reports' / 'Unified_Report.md'
            self._write_unified_report(report, report_file)

            return report

        except Exception as e:
            error_msg = f"Failed to generate unified report: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def _write_unified_report(self, report: dict, report_file: Path):
        """Write unified report to markdown file"""
        try:
            report_file.parent.mkdir(parents=True, exist_ok=True)

            content = f"""# Unified Domain Report

**Generated:** {report['generated']}

---

## Overview

Total tasks across all domains: **{report['totals']['all_tasks']}**

---

## Business Domain

- **Inbox:** {report['business']['inbox']} tasks
- **Needs Action:** {report['business']['needs_action']} tasks
- **Done:** {report['business']['done']} tasks
- **Total:** {report['business']['total']} tasks

---

## Personal Domain

- **Inbox:** {report['personal']['inbox']} tasks
- **Needs Action:** {report['personal']['needs_action']} tasks
- **Done:** {report['personal']['done']} tasks
- **Total:** {report['personal']['total']} tasks

---

## Cross-Domain Tasks

- **Pending:** {report['cross_domain']} tasks

---

## Summary Statistics

| Domain | Inbox | Needs Action | Done | Total |
|--------|-------|--------------|------|-------|
| Business | {report['business']['inbox']} | {report['business']['needs_action']} | {report['business']['done']} | {report['business']['total']} |
| Personal | {report['personal']['inbox']} | {report['personal']['needs_action']} | {report['personal']['done']} | {report['personal']['total']} |
| **Total** | **{report['totals']['inbox']}** | **{report['totals']['needs_action']}** | **{report['totals']['done']}** | **{report['totals']['all_tasks']}** |

---

## Work-Life Balance

- **Business Tasks:** {report['business']['total']} ({report['business']['total'] / report['totals']['all_tasks'] * 100:.1f}%)
- **Personal Tasks:** {report['personal']['total']} ({report['personal']['total'] / report['totals']['all_tasks'] * 100:.1f}%)
- **Cross-Domain:** {report['cross_domain']} ({report['cross_domain'] / report['totals']['all_tasks'] * 100:.1f}%)

---

*Generated by Cross-Domain Router*
"""

            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Unified report written to {report_file}")

        except Exception as e:
            logger.error(f"Error writing unified report: {e}")

    def _log_routing(self, task_name: str, source: str, destination: str):
        """Log task routing"""
        try:
            log_dir = Path(__file__).parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'routing.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] ROUTING: {task_name} | {source} → {destination}\n")

        except Exception as e:
            logger.error(f"Failed to log routing: {e}")

    def _log_business_activity(self, message: str):
        """Log to business log"""
        try:
            log_dir = Path(__file__).parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'business.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] CROSS_DOMAIN: {message}\n")

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
                f.write(f"[{timestamp}] CROSS_DOMAIN_ERROR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python cross_domain_router.py <command> [args]"
        }))
        sys.exit(1)

    command = sys.argv[1]
    router = CrossDomainRouter()

    if command == 'route':
        if len(sys.argv) < 3:
            result = {"error": "Usage: python cross_domain_router.py route <task_file>"}
        else:
            task_file = Path(sys.argv[2])
            source_domain = sys.argv[3] if len(sys.argv) > 3 else None
            result = router.route_task(task_file, source_domain)

    elif command == 'process-cross-domain':
        result = router.process_cross_domain_tasks()

    elif command == 'unified-report':
        result = router.generate_unified_report()

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
