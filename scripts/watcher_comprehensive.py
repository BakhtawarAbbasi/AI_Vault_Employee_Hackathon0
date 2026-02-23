#!/usr/bin/env python3
"""
Comprehensive File Watcher
Monitors multiple sources including file system, and can be extended for web sources.
"""

import os
import sys
import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    def __init__(self, vault_path="AI_Employee_Vault"):
        self.vault_path = vault_path
        self.needs_action_path = os.path.join(vault_path, "Needs_Action")
        os.makedirs(self.needs_action_path, exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith('.md'):
            print(json.dumps({"event": "file_created", "path": event.src_path}))
            self.process_new_file(event.src_path)

    def process_new_file(self, file_path):
        """Process the new markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(json.dumps({"error": f"Error reading file {file_path}: {str(e)}"}))
            return

        # Extract title from content
        title = "Untitled Task"
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('# '):
                title = line.strip()[2:]
                break

        # Create a summary
        summary = content.strip()
        if len(summary) > 200:
            summary = summary[:197] + '...'

        # Generate timestamp for the action file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the action file name
        original_filename = os.path.basename(file_path)
        action_filename = f"FILE_INBOX_{timestamp}_{original_filename}"
        action_path = os.path.join(self.vault_path, 'Needs_Action', action_filename)

        # Create the action content
        action_content = f"""---
type: file_inbox
source: {original_filename}
timestamp: {datetime.now().isoformat()}
status: pending
---

# New File in Inbox: {title}

## Original Content
```
{content.strip()}
```

## Summary
{summary}

## Recommended Actions
- [ ] Review the content carefully
- [ ] Create a detailed plan if needed
- [ ] Execute required tasks
- [ ] Move to Done when complete

---
File detected in Inbox on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        # Write the action file
        with open(action_path, 'w', encoding='utf-8') as f:
            f.write(action_content)

        print(json.dumps({
            "info": f"Created action file for inbox item: {action_filename}",
            "original_file": original_filename
        }))


def main():
    """Main function to start the comprehensive watcher"""
    vault_path = "AI_Employee_Vault"
    inbox_path = os.path.join(vault_path, "Inbox")

    # Create necessary directories
    os.makedirs(inbox_path, exist_ok=True)
    os.makedirs(os.path.join(vault_path, "Needs_Action"), exist_ok=True)

    print(json.dumps({"info": f"Starting comprehensive watcher for {inbox_path}"}))

    # Set up the file system watcher
    event_handler = InboxHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, inbox_path, recursive=False)

    observer.start()

    try:
        print(json.dumps({"info": "Comprehensive watcher started, press Ctrl+C to stop"}))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(json.dumps({"info": "Comprehensive watcher stopped"}))

    observer.join()


if __name__ == "__main__":
    main()