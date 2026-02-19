import os
from datetime import datetime

def check_and_rotate_log(file_path, max_size=1024*1024):  # Default 1MB in bytes
    """
    Check if a log file is larger than max_size and rotate it if needed.

    Args:
        file_path (str): Path to the log file to check
        max_size (int): Maximum file size in bytes (default 1MB)
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Log file does not exist: {file_path}")
        return

    # Get the current file size
    file_size = os.path.getsize(file_path)

    # Check if file is larger than the max size
    if file_size > max_size:
        # Create a timestamp for the backup file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Split the file path into directory, name, and extension
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)

        # Create the new backup file name with timestamp
        backup_filename = f"{name}_{timestamp}{ext}"
        backup_path = os.path.join(directory, backup_filename)

        # Rename the large file to the backup name
        os.rename(file_path, backup_path)

        # Create a new empty log file with the original name
        with open(file_path, 'w') as f:
            # For System_Log.md, we'll create with the basic header
            if file_path.endswith("System_Log.md"):
                f.write("# System Log\n\n## Activity Log\n")
            else:
                # For other log files, create empty
                f.write("")

        print(f"Rotated log file: {filename} -> {backup_filename}")
    else:
        print(f"Log file {file_path} is within size limit ({file_size} bytes)")


def main():
    """
    Main function that checks and rotates large log files.
    """
    print("Starting log manager...")
    print("Checking for large log files...")

    # Check System_Log.md
    check_and_rotate_log("System_Log.md")

    # Check Logs/watcher_error.log, creating Logs directory if needed
    log_dir = os.path.dirname("Logs/watcher_error.log")
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created directory: {log_dir}")

    check_and_rotate_log("Logs/watcher_error.log")

    print("Log management completed.")


if __name__ == "__main__":
    main()