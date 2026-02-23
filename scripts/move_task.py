#!/usr/bin/env python3
"""
Vault File Manager Skill
Move files between vault folders: Inbox, Needs_Action, Done
"""

import os
import sys
import shutil
import json


def move_task(source_folder, dest_folder, filename):
    """Move a task file between vault folders"""
    base_path = "AI_Employee_Vault"

    # Define source and destination paths
    source_path = os.path.join(base_path, source_folder, filename)
    dest_path = os.path.join(base_path, dest_folder, filename)

    # Check if source file exists
    if not os.path.exists(source_path):
        return {"error": f"Source file does not exist: {source_path}"}

    # Create destination folder if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        # Move the file
        shutil.move(source_path, dest_path)
        return {"success": f"Moved {filename} from {source_folder} to {dest_folder}"}
    except Exception as e:
        return {"error": f"Failed to move file: {str(e)}"}


def main():
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Usage: python move_task.py <source_folder> <dest_folder> <filename>"}))
        print(json.dumps({"note": "Folders: Inbox, Needs_Action, Done"}))
        sys.exit(1)

    source_folder = sys.argv[1]
    dest_folder = sys.argv[2]
    filename = sys.argv[3]

    valid_folders = ["Inbox", "Needs_Action", "Done"]
    if source_folder not in valid_folders or dest_folder not in valid_folders:
        print(json.dumps({"error": f"Invalid folder. Use: {valid_folders}"}))
        sys.exit(1)

    result = move_task(source_folder, dest_folder, filename)
    print(json.dumps(result))


if __name__ == "__main__":
    main()