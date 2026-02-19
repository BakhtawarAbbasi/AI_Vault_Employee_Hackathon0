import os
import shutil
from datetime import datetime

def process_tasks():
    """Process all tasks in Needs_Action folder"""
    print("Processing tasks...")

    # Check if Needs_Action folder exists
    if not os.path.exists("Needs_Action"):
        print("Needs_Action folder not found.")
        return

    task_files = [f for f in os.listdir("Needs_Action") if f.endswith('.md')]

    if not task_files:
        print("No tasks found in Needs_Action folder.")
        return

    for task_file in task_files:
        task_path = os.path.join("Needs_Action", task_file)

        # Read the task file
        with open(task_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Processing task: {task_file}")

        # Extract task information from YAML frontmatter
        lines = content.split('\n')
        yaml_end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:  # Second occurrence of ---
                yaml_end_idx = i
                break

        # Extract filename from the task title in the content
        filename = None
        for line in lines:
            if line.strip().startswith('# Review File:'):
                filename = line.split(':', 1)[1].strip()
                break

        # If not found in title, try the old format as fallback
        if not filename:
            for line in lines:
                if line.strip().startswith('filename:'):
                    filename = line.split(':', 1)[1].strip()
                    break

        # Update the status to 'completed' in the YAML frontmatter
        updated_content = content.replace('status: pending', 'status: completed')

        # Write the updated content back to the file
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Move the file to Done folder
        done_path = os.path.join("Done", task_file)
        shutil.move(task_path, done_path)
        print(f"Moved {task_file} to Done folder")

        # Update Dashboard.md
        update_dashboard(filename if filename else task_file)

        # Add entry to System_Log.md
        add_to_system_log(filename if filename else task_file)

    print("All tasks processed and moved to Done folder.")

def update_dashboard(task_name):
    """Update Dashboard.md with completed task"""
    if not os.path.exists("Dashboard.md"):
        print("Dashboard.md not found.")
        return

    with open("Dashboard.md", 'r', encoding='utf-8') as f:
        content = f.read()

    # Add the task to Completed Tasks section
    completed_section_start = content.find("## Completed Tasks")
    if completed_section_start != -1:
        # Find the next section or end of file
        next_section_start = content.find("## ", completed_section_start + 1)
        if next_section_start == -1:
            next_section_start = len(content)

        # Extract completed tasks section
        completed_section = content[completed_section_start:next_section_start]
        completed_tasks_lines = completed_section.split('\n')

        # Find where actual completed tasks start (skip the section header)
        tasks_start_idx = 0
        for i, line in enumerate(completed_tasks_lines):
            if line.strip().startswith('- [x]'):
                tasks_start_idx = i
                break

        # Create the new completed task entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_completed_task = f"- [x] {task_name} (Completed: {timestamp})"

        # Build the updated content
        before_completed = content[:completed_section_start]
        after_completed = content[next_section_start:]

        # Insert the new completed task at the beginning of the list
        updated_completed = "## Completed Tasks\n"
        updated_completed += new_completed_task + "\n"
        for line in completed_tasks_lines[1:]:  # Skip the section header
            if line.strip():  # Add non-empty lines
                updated_completed += line + "\n"

        updated_content = before_completed + updated_completed + after_completed
    else:
        updated_content = content  # If section not found, don't modify anything

    # Remove the task from Pending Tasks if it exists
    pending_section_start = updated_content.find("## Pending Tasks")
    if pending_section_start != -1:
        # Find the end of the pending tasks section
        next_section_start = updated_content.find("## ", pending_section_start + 1)
        if next_section_start == -1:
            next_section_start = len(updated_content)

        pending_section = updated_content[pending_section_start:next_section_start]
        pending_tasks_lines = pending_section.split('\n')

        # Filter out the completed task
        filtered_lines = []
        for line in pending_tasks_lines:
            if task_name not in line:
                filtered_lines.append(line)
            elif not line.strip().startswith('- [ ]'):  # Keep section header and other formatting
                filtered_lines.append(line)

        # Rebuild the content with filtered pending tasks
        before_pending = updated_content[:pending_section_start]
        after_pending = updated_content[next_section_start:]

        updated_pending = "## Pending Tasks\n"
        for line in filtered_lines[1:]:  # Skip the section header
            if line.strip():  # Add non-empty lines
                updated_pending += line + "\n"

        updated_content = before_pending + updated_pending + after_pending

    # Write updated content back to Dashboard.md
    with open("Dashboard.md", 'w', encoding='utf-8') as f:
        f.write(updated_content)

def add_to_system_log(task_name):
    """Add entry to System_Log.md"""
    if not os.path.exists("System_Log.md"):
        print("System_Log.md not found.")
        return

    with open("System_Log.md", 'r', encoding='utf-8') as f:
        content = f.read()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_log_entry = f"\n### [{timestamp}]\n- Completed task: {task_name}\n"

    # Find where to insert the new entry (after the first ### or at the end of main content)
    activity_log_start = content.find("## Activity Log")
    if activity_log_start != -1:
        # Insert after the Activity Log header
        insertion_point = activity_log_start + len("## Activity Log")
        # Skip any existing entries to add the new one at the most recent position
        updated_content = content[:insertion_point] + new_log_entry + content[insertion_point:]
    else:
        updated_content = content + new_log_entry

    with open("System_Log.md", 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    process_tasks()