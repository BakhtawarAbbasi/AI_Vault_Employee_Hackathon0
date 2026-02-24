# Personal Tasks Skill

Manage personal tasks separate from business tasks.

## Trigger Phrases

- "Create personal task"
- "List personal tasks"
- "Process personal inbox"
- "Complete personal task"
- "Show my personal tasks"

## What This Skill Does

This skill manages personal tasks in a separate domain from business tasks. It:

1. Creates personal tasks in `AI_Employee_Vault/Personal/Inbox/`
2. Processes inbox and moves tasks to appropriate folders
3. Lists tasks by status (inbox, needs_action, done)
4. Marks tasks as complete
5. Logs all activity to business.log
6. Maintains separation between personal and business domains

## Directory Structure

```
AI_Employee_Vault/Personal/
├── Inbox/           # New personal tasks
├── Needs_Action/    # Tasks requiring action
├── Done/            # Completed tasks
└── Notes/           # Personal notes
```

## Usage

### Create a Personal Task

```bash
python scripts/personal_tasks.py create "Task Title" "Task description" "high"
```

**Priority levels:** low, medium, high

### Process Inbox

```bash
python scripts/personal_tasks.py process-inbox
```

This automatically:
- Reads tasks from Personal/Inbox/
- Moves tasks with unchecked items to Needs_Action/
- Moves completed tasks to Done/

### List Tasks

```bash
# List all tasks
python scripts/personal_tasks.py list all

# List inbox tasks only
python scripts/personal_tasks.py list inbox

# List tasks needing action
python scripts/personal_tasks.py list needs_action

# List completed tasks
python scripts/personal_tasks.py list done
```

### Complete a Task

```bash
python scripts/personal_tasks.py complete "AI_Employee_Vault/Personal/Needs_Action/task_file.md"
```

## Response Format

### Create Task Success

```json
{
  "success": true,
  "message": "Personal task created",
  "task_file": "AI_Employee_Vault/Personal/Inbox/20260224_143000_Task_Title.md",
  "title": "Task Title",
  "priority": "high"
}
```

### List Tasks Success

```json
{
  "success": true,
  "tasks": [
    {
      "file": "AI_Employee_Vault/Personal/Needs_Action/task1.md",
      "name": "task1.md",
      "title": "Task Title",
      "status": "needs_action"
    }
  ],
  "count": 1
}
```

### Error

```json
{
  "error": "Error message description"
}
```

## Task File Format

When you create a task, it's saved in this format:

```markdown
# Task Title

**Created:** 2026-02-24 14:30:00
**Priority:** high
**Status:** Pending

## Description

Task description goes here

## Notes

(Add notes here)

## Completion

- [ ] Task completed
```

## Features

### Automatic Processing

The `process-inbox` command automatically:
- Detects tasks with unchecked items (`- [ ]`)
- Detects tasks with TODO markers
- Moves actionable tasks to Needs_Action/
- Moves completed tasks to Done/

### Priority Levels

- **high**: Urgent personal tasks
- **medium**: Normal priority (default)
- **low**: Can wait

### Completion Tracking

When you complete a task, it:
- Moves to Done/ folder
- Adds completion timestamp
- Logs to business.log

### Separation from Business

Personal tasks are completely separate from business tasks:
- Different directory structure
- Separate workflow
- Clear domain boundaries
- Logged with PERSONAL prefix

## Integration

### Scheduler Integration

Add to `scripts/scheduler.py` for automatic processing:

```python
# Process personal inbox every hour
scheduler.add_task(
    name="process_personal_inbox",
    interval_seconds=3600,  # Hourly
    command="scripts/personal_tasks.py",
    args=["process-inbox"]
)
```

### Ralph Wiggum Integration

Personal tasks can be processed by the Ralph Wiggum autonomous loop for automatic completion.

### CEO Briefing Integration

Personal task statistics can be included in CEO briefings to show work-life balance.

## Logging

All personal task activity is logged to:

### business.log

```
[2026-02-24 14:30:00] PERSONAL: Created personal task: Buy groceries
[2026-02-24 15:00:00] PERSONAL: Processed 3 personal tasks from inbox
[2026-02-24 16:00:00] PERSONAL: Completed personal task: buy_groceries.md
```

### error.log

```
[2026-02-24 14:30:00] PERSONAL_ERROR: Failed to create personal task: Permission denied
```

## Security

- All tasks stored locally
- No external API calls
- Complete audit trail
- Separate from business data
- Privacy maintained

## Use Cases

### Personal Errands

```bash
python scripts/personal_tasks.py create "Buy groceries" "Milk, eggs, bread" "medium"
```

### Home Tasks

```bash
python scripts/personal_tasks.py create "Fix leaky faucet" "Kitchen sink needs repair" "high"
```

### Personal Goals

```bash
python scripts/personal_tasks.py create "Exercise 3x this week" "Gym sessions on Mon/Wed/Fri" "medium"
```

### Reading List

```bash
python scripts/personal_tasks.py create "Read book" "Finish 'Atomic Habits'" "low"
```

## Examples

### Example 1: Create and Process

```bash
# Create a task
python scripts/personal_tasks.py create "Call dentist" "Schedule checkup appointment" "high"

# Process inbox (moves to Needs_Action)
python scripts/personal_tasks.py process-inbox

# List tasks needing action
python scripts/personal_tasks.py list needs_action
```

### Example 2: Complete a Task

```bash
# List tasks
python scripts/personal_tasks.py list needs_action

# Complete specific task
python scripts/personal_tasks.py complete "AI_Employee_Vault/Personal/Needs_Action/20260224_143000_Call_dentist.md"

# Verify completion
python scripts/personal_tasks.py list done
```

### Example 3: Weekly Review

```bash
# See all personal tasks
python scripts/personal_tasks.py list all

# Process any new inbox items
python scripts/personal_tasks.py process-inbox

# Review completed tasks
python scripts/personal_tasks.py list done
```

## Files

- **Script:** `scripts/personal_tasks.py`
- **Inbox:** `AI_Employee_Vault/Personal/Inbox/`
- **Needs Action:** `AI_Employee_Vault/Personal/Needs_Action/`
- **Done:** `AI_Employee_Vault/Personal/Done/`
- **Notes:** `AI_Employee_Vault/Personal/Notes/`
- **Business Log:** `AI_Employee_Vault/Logs/business.log`
- **Error Log:** `AI_Employee_Vault/Logs/error.log`

## API Reference

### create_task(title, description, priority)

Creates a new personal task.

**Parameters:**
- `title` (string): Task title
- `description` (string): Task description
- `priority` (string): Priority level (low, medium, high)

**Returns:** Task details or error

### process_inbox()

Processes personal inbox tasks.

**Returns:** Processing results or error

### list_tasks(status)

Lists personal tasks.

**Parameters:**
- `status` (string): Filter by status (inbox, needs_action, done, all)

**Returns:** List of tasks or error

### complete_task(task_file)

Marks a task as complete.

**Parameters:**
- `task_file` (string): Path to task file

**Returns:** Success status or error

## Future Enhancements

- Task reminders
- Recurring tasks
- Task dependencies
- Time tracking
- Task categories/tags
- Search functionality
- Mobile app integration
- Calendar integration

## Status

✅ **Production Ready**
- Personal domain separation
- Complete workflow
- Automatic processing
- Scheduler integration
- Business log integration
- Error handling

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Operational ✅
