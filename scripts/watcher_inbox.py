#!/usr/bin/env python3
"""
Vault Inbox Watcher
Continuously monitors vault/Inbox for new .md files and triggers AI processing.
"""

import os
import time
import json
from datetime import datetime
import subprocess
import sys

class VaultInboxWatcher:
    def __init__(self, inbox_path="vault/Inbox", log_path="logs/actions.log", interval_range=(10, 30)):
        self.inbox_path = inbox_path
        self.log_path = log_path
        self.interval_range = interval_range  # (min, max) seconds

        # Ensure directories exist
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        os.makedirs(inbox_path, exist_ok=True)

        # Track processed files to avoid duplicates
        self.processed_files_path = "logs/processed_files.json"
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self):
        """Load the set of already processed files from disk"""
        if os.path.exists(self.processed_files_path):
            try:
                with open(self.processed_files_path, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    def _save_processed_files(self):
        """Save the set of processed files to disk"""
        os.makedirs(os.path.dirname(self.processed_files_path), exist_ok=True)
        with open(self.processed_files_path, 'w') as f:
            json.dump(list(self.processed_files), f)

    def _log_action(self, message):
        """Log action to the actions log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        # Also print to console for real-time monitoring
        print(log_entry.strip())

    def get_new_files(self):
        """Get a list of new .md files in the inbox that haven't been processed"""
        if not os.path.exists(self.inbox_path):
            return []

        current_files = []
        for filename in os.listdir(self.inbox_path):
            if filename.endswith('.md'):
                filepath = os.path.join(self.inbox_path, filename)
                if os.path.isfile(filepath):
                    current_files.append(filepath)

        # Filter out files we've already processed
        new_files = []
        for filepath in current_files:
            filename = os.path.basename(filepath)
            if filename not in self.processed_files:
                new_files.append(filepath)

        return new_files

    def trigger_ai_processing(self):
        """Trigger the AI processing workflow (equivalent to run_ai_employee.py --once)"""
        try:
            # This is a placeholder - in a real implementation you'd call the actual AI processing
            # For now, we'll just simulate the processing with a log entry
            self._log_action("AI processing workflow triggered")

            # If run_ai_employee.py exists, you could call it like this:
            # result = subprocess.run([sys.executable, "run_ai_employee.py", "--once"],
            #                        capture_output=True, text=True)
            # if result.returncode == 0:
            #     self._log_action(f"AI processing completed successfully")
            # else:
            #     self._log_action(f"AI processing failed: {result.stderr}")
        except Exception as e:
            self._log_action(f"Error triggering AI processing: {str(e)}")

    def process_file(self, filepath):
        """Process a single file"""
        filename = os.path.basename(filepath)
        self._log_action(f"New file detected: {filename}")

        # Add to processed files to prevent duplicates
        self.processed_files.add(filename)
        self._save_processed_files()

        # Trigger AI processing workflow
        self.trigger_ai_processing()

    def run(self):
        """Run the continuous monitoring loop"""
        self._log_action("Starting Vault Inbox Watcher")
        self._log_action(f"Monitoring: {self.inbox_path}")

        try:
            while True:
                # Get new files
                new_files = self.get_new_files()

                if new_files:
                    self._log_action(f"Found {len(new_files)} new file(s)")
                    for filepath in new_files:
                        self.process_file(filepath)
                else:
                    # No new files, just continue
                    pass

                # Wait for a random interval between min and max
                import random
                wait_time = random.uniform(*self.interval_range)

                # Small optimization to not sleep if we just processed files
                time.sleep(wait_time)

        except KeyboardInterrupt:
            self._log_action("Watcher stopped by user")
        except Exception as e:
            self._log_action(f"Error in watcher: {str(e)}")
            raise


def main():
    """Main function to run the vault inbox watcher"""
    # Create watcher instance
    watcher = VaultInboxWatcher(
        inbox_path="vault/Inbox",
        log_path="logs/actions.log",
        interval_range=(10, 30)  # 10-30 seconds interval
    )

    # Run the watcher
    watcher.run()


if __name__ == "__main__":
    main()