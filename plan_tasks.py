import os
from datetime import datetime

def make_plan_for_tasks():
    """Create a plan for all tasks in Needs_Action folder"""
    print("Creating a plan for pending tasks...")

    # Check if Needs_Action folder exists
    if not os.path.exists("Needs_Action"):
        print("Needs_Action folder not found. No tasks to plan.")
        return

    task_files = [f for f in os.listdir("Needs_Action") if f.endswith('.md')]

    if not task_files:
        print("No tasks found in Needs_Action folder.")
        return

    # Create Plans directory if it doesn't exist
    if not os.path.exists("Plans"):
        os.makedirs("Plans")

    # Read and analyze all task files
    task_details = []
    for task_file in task_files:
        task_path = os.path.join("Needs_Action", task_file)

        with open(task_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract task information
        lines = content.split('\n')

        # Extract YAML frontmatter to get task type
        task_type = "unknown"
        status = "unknown"
        priority = "unknown"
        related_files = []

        yaml_started = False
        yaml_ended = False
        for line in lines:
            if line.strip() == '---':
                if not yaml_started:
                    yaml_started = True
                elif yaml_started and not yaml_ended:
                    yaml_ended = True
                    continue
            elif yaml_started and not yaml_ended:
                if line.strip().startswith('type:'):
                    task_type = line.split(':', 1)[1].strip()
                elif line.strip().startswith('status:'):
                    status = line.split(':', 1)[1].strip()
                elif line.strip().startswith('priority:'):
                    priority = line.split(':', 1)[1].strip()
                elif line.strip().startswith('related files:'):
                    try:
                        files_part = line.split(':', 1)[1].strip()
                        # Simple parsing of related files list
                        if files_part.startswith('[') and files_part.endswith(']'):
                            files_content = files_part[1:-1]  # Remove brackets
                            related_files = [f.strip().strip('"').strip("'") for f in files_content.split(',')]
                    except:
                        related_files = []
            else:
                # Skip YAML parsing after it's ended
                if yaml_ended:
                    break

        # Extract title
        title = "Unknown"
        for line in lines:
            if line.strip().startswith('# '):
                title = line.strip()[2:]
                break

        task_details.append({
            'filename': task_file,
            'title': title,
            'type': task_type,
            'status': status,
            'priority': priority,
            'related_files': related_files
        })

    # Create the plan file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plan_filename = f"Plan_{timestamp}.md"
    plan_path = os.path.join("Plans", plan_filename)

    # Generate plan content
    plan_content = f"""# Task Plan - {timestamp}

## Summary of Pending Tasks

"""
    # Add summary of tasks
    task_summary = []
    for task in task_details:
        task_summary.append(f"- **{task['title']}** ({task['type']}) - Priority: {task['priority']}")

    plan_content += "\n".join(task_summary)
    plan_content += "\n\n## Suggested Order of Execution\n\n"

    # Group tasks by priority
    high_priority = [t for t in task_details if t['priority'] == 'high']
    medium_priority = [t for t in task_details if t['priority'] == 'medium']
    low_priority = [t for t in task_details if t['priority'] == 'low']
    unknown_priority = [t for t in task_details if t['priority'] not in ['high', 'medium', 'low']]

    execution_order = []
    # Add execution order based on priority
    if high_priority:
        execution_order.append("### High Priority Tasks")
        for task in high_priority:
            execution_order.append(f"- {task['title']}")
        execution_order.append("")

    if medium_priority:
        execution_order.append("### Medium Priority Tasks")
        for task in medium_priority:
            execution_order.append(f"- {task['title']}")
        execution_order.append("")

    if low_priority:
        execution_order.append("### Low Priority Tasks")
        for task in low_priority:
            execution_order.append(f"- {task['title']}")
        execution_order.append("")

    if unknown_priority:
        execution_order.append("### Other Tasks")
        for task in unknown_priority:
            execution_order.append(f"- {task['title']}")
        execution_order.append("")

    plan_content += "\n".join(execution_order)
    plan_content += "\n## Risks or Unclear Items\n\n"

    # Identify any risks or unclear items
    risks = []
    for task in task_details:
        if task['priority'] == 'unknown':
            risks.append(f"- Task '{task['title']}' has unknown priority")
        if task['type'] == 'unknown':
            risks.append(f"- Task '{task['title']}' has unknown type")
        if not task['related_files'] or task['related_files'] == ['']:
            risks.append(f"- Task '{task['title']}' has no related files specified")

    if risks:
        plan_content += "\n".join(risks)
    else:
        plan_content += "- No specific risks identified"

    plan_content += f"""

## Strategy

Based on the pending tasks, the recommended strategy is to address high-priority tasks first, particularly focusing on any file review tasks that might be blocking other operations. The tasks should be executed in the suggested order above, with attention to any risks or unclear items identified. For tasks with unknown priority or type, further clarification may be needed before execution.

There are {len(task_details)} total pending tasks to address.
"""

    # Write the plan to file
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan_content)

    print(f"Plan created: {plan_filename}")
    print(f"Total tasks analyzed: {len(task_details)}")


if __name__ == "__main__":
    make_plan_for_tasks()