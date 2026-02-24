# Personal Domain - README

## Overview

The Personal domain provides a separate workspace for managing personal tasks, notes, and activities distinct from business operations.

## Directory Structure

```
AI_Employee_Vault/Personal/
├── Inbox/           # New personal tasks and items
├── Needs_Action/    # Tasks requiring your attention
├── Done/            # Completed personal tasks
└── Notes/           # Personal notes and references
```

## Purpose

This domain separates personal life from business operations:

- **Personal Tasks**: Errands, home tasks, personal goals
- **Personal Notes**: Ideas, reminders, personal references
- **Work-Life Balance**: Clear separation of concerns
- **Privacy**: Personal items kept separate from business data

## Workflow

### 1. Create Personal Tasks

Tasks start in the `Inbox/` folder:

```bash
python scripts/personal_tasks.py create "Task Title" "Description" "priority"
```

### 2. Process Inbox

Automatically sort tasks:

```bash
python scripts/personal_tasks.py process-inbox
```

Tasks with action items move to `Needs_Action/`, completed tasks move to `Done/`.

### 3. Work on Tasks

Review tasks needing action:

```bash
python scripts/personal_tasks.py list needs_action
```

### 4. Complete Tasks

Mark tasks as done:

```bash
python scripts/personal_tasks.py complete "path/to/task.md"
```

## Integration

### Scheduler

Add to `scripts/scheduler.py` for automatic processing:

```python
scheduler.add_task(
    name="process_personal_inbox",
    interval_seconds=3600,  # Hourly
    command="scripts/personal_tasks.py",
    args=["process-inbox"]
)
```

### Logging

All personal activity is logged with `PERSONAL:` prefix in `business.log`.

## Use Cases

- **Errands**: Shopping lists, appointments, calls to make
- **Home Tasks**: Repairs, maintenance, cleaning
- **Personal Goals**: Exercise, reading, hobbies
- **Family**: Events, reminders, planning
- **Health**: Medical appointments, prescriptions
- **Finance**: Personal bills, budgeting (separate from business)

## Privacy

- All data stored locally
- Separate from business domain
- No external sharing
- Complete control

## Examples

### Create a Shopping List

```bash
python scripts/personal_tasks.py create "Grocery Shopping" "Milk, eggs, bread, coffee" "medium"
```

### Schedule Personal Appointment

```bash
python scripts/personal_tasks.py create "Dentist Appointment" "Call to schedule 6-month checkup" "high"
```

### Track Personal Goal

```bash
python scripts/personal_tasks.py create "Exercise This Week" "Gym 3x: Mon/Wed/Fri" "medium"
```

## Notes Folder

Use `Notes/` for:
- Personal ideas
- Reference information
- Quick thoughts
- Reading lists
- Project ideas

Simply create `.md` files in the `Notes/` folder.

## Best Practices

1. **Regular Processing**: Process inbox daily or weekly
2. **Clear Titles**: Use descriptive task titles
3. **Set Priorities**: Mark urgent items as high priority
4. **Complete Promptly**: Move done tasks to Done/ folder
5. **Review Weekly**: Check all personal tasks weekly

## Separation from Business

The Personal domain is completely separate:

- Different directory structure
- Separate workflow
- Independent processing
- Clear boundaries

This ensures:
- Work-life balance
- Privacy protection
- Organized task management
- Reduced cognitive load

## Status

✅ **Operational**
- Directory structure created
- Task handler implemented
- Workflow established
- Scheduler integration ready

---

**Created:** 2026-02-24
**Status:** Production Ready ✅
