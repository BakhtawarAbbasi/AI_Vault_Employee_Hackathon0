import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Event detected: {event}")
        print(f"Is directory: {event.is_directory}")
        print(f"Source path: {event.src_path}")

        if event.is_directory:
            return

        print(f"Checking if file ends with .md: {event.src_path.endswith('.md')}")

        # Check if the new file is a markdown file
        if event.src_path.endswith('.md'):
            print(f"New file detected: {os.path.basename(event.src_path)}")
            self.process_new_file(event.src_path)

    def process_new_file(self, file_path):
        """Process the new markdown file"""
        print(f"Processing file: {file_path}")
        # Read the content of the new file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"Content read successfully, length: {len(content)}")
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # Extract title from content (first line starting with # if it exists)
        title = "Untitled Task"
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('# '):
                title = line.strip()[2:]  # Remove '# ' prefix
                print(f"Found title: {title}")
                break

        # Create a summary based on the content
        # Take first 200 characters of content as summary
        summary = content.strip()
        if len(summary) > 200:
            summary = summary[:197] + '...'

        # Generate timestamp for the response file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the response file name
        original_filename = os.path.basename(file_path)
        response_filename = f"response_{timestamp}_{original_filename}"

        # Define the path for the response file in Needs_Action folder
        response_path = os.path.join('vault', 'Needs_Action', response_filename)
        print(f"Response path: {response_path}")

        # Create the response content with title and summary
        response_content = f"""# Response to: {title}

## Summary of Original Task
{summary}

## Action Required
[Add specific action items based on the original task]

## Status
- [ ] Review original task
- [ ] Complete required action
- [ ] Move to Done when finished

---
File processed on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Original file: {original_filename}
"""

        # Write the response file to Needs_Action folder
        try:
            with open(response_path, 'w', encoding='utf-8') as f:
                f.write(response_content)
            print(f"Response file created: {response_filename}")
        except Exception as e:
            print(f"Error writing response file: {e}")

def main():
    # Create the vault/Inbox and vault/Needs_Action directories if they don't exist
    os.makedirs(os.path.join('vault', 'Inbox'), exist_ok=True)
    os.makedirs(os.path.join('vault', 'Needs_Action'), exist_ok=True)

    # Create the event handler
    event_handler = InboxHandler()

    # Create an observer
    observer = Observer()

    # Schedule the observer to watch the Inbox folder
    watch_path = os.path.join('vault', 'Inbox')
    print(f"Setting up watcher for: {watch_path}")
    observer.schedule(event_handler, watch_path, recursive=False)

    print("Starting file watcher...")
    print(f"Watching: {watch_path}")
    print("Press Ctrl+C to stop")

    # Start the observer
    observer.start()

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer when interrupted
        observer.stop()
        print("\nFile watcher stopped.")

    # Wait for the observer to finish
    observer.join()

if __name__ == "__main__":
    main()