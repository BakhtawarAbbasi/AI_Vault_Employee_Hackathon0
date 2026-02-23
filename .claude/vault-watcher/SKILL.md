# Vault Watcher Skill

## Purpose
This skill implements a continuous file system watcher that monitors the vault/Inbox folder for new markdown files and triggers AI processing workflows when files appear.

## Functionality
- Continuously monitors vault/Inbox for new .md files
- Logs all detections to logs/actions.log
- Triggers AI processing workflow (equivalent to run_ai_employee.py --once)
- Prevents duplicate processing of the same file
- Runs efficiently with 10-30 second intervals

## Technical Implementation
- Uses Python file system monitoring
- Implements file tracking to prevent duplicates
- Includes error handling and logging
- Lightweight and production-ready design

## Usage
Run the watcher script to start monitoring:
```
python scripts/watcher_inbox.py
```

The script will run continuously, monitoring for new files and processing them as they appear.

## Configuration
- Polling interval: 10-30 seconds (configurable)
- Target folder: vault/Inbox
- Target file type: .md files
- Log file: logs/actions.log

## Process Flow
1. Check vault/Inbox for new .md files
2. Compare against previously processed files
3. Process only new/unprocessed files
4. Log detection and processing to actions.log
5. Trigger AI processing workflow
6. Record processed files to avoid duplicates
7. Wait specified interval before next check