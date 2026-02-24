# Cross-Domain Integration Skill

Manage tasks that span both Personal and Business domains.

## Trigger Phrases

- "Route this task"
- "Cross-domain task"
- "Process cross-domain tasks"
- "Unified report"
- "Show all tasks"
- "Work-life balance report"

## What This Skill Does

This skill manages tasks that have both personal and business components. It:

1. Classifies tasks as personal, business, or cross-domain
2. Routes tasks to appropriate domains
3. Creates linked tasks across domains
4. Generates unified reports across all domains
5. Tracks work-life balance

## Usage

### Route a Task

```bash
python scripts/cross_domain_router.py route "path/to/task.md" "source_domain"
```

### Process Cross-Domain Tasks

```bash
python scripts/cross_domain_router.py process-cross-domain
```

This automatically:
- Reads tasks from Cross_Domain folder
- Creates linked tasks in both Personal and Business domains
- Archives original cross-domain task

### Generate Unified Report

```bash
python scripts/cross_domain_router.py unified-report
```

## Response Format

### Route Task Success

```json
{
  "success": true,
  "task": "task_file.md",
  "source": "business",
  "destination": "personal",
  "classification": "personal"
}
```

### Unified Report Success

```json
{
  "success": true,
  "generated": "2026-02-24T09:14:00Z",
  "business": {
    "inbox": 5,
    "needs_action": 3,
    "done": 12,
    "total": 20
  },
  "personal": {
    "inbox": 2,
    "needs_action": 1,
    "done": 8,
    "total": 11
  },
  "cross_domain": 1,
  "totals": {
    "inbox": 7,
    "needs_action": 4,
    "done": 20,
    "all_tasks": 32
  }
}
```

## Directory Structure

```
AI_Employee_Vault/
├── Inbox/                    # Business inbox
├── Needs_Action/             # Business needs action
├── Done/                     # Business done
├── Personal/
│   ├── Inbox/               # Personal inbox
│   ├── Needs_Action/        # Personal needs action
│   └── Done/                # Personal done
├── Cross_Domain/            # Cross-domain tasks
│   └── Archive/             # Processed cross-domain tasks
└── Reports/
    └── Unified_Report.md    # Unified domain report
```

## Features

### Automatic Classification

The router uses keyword analysis to classify tasks:

**Personal Keywords:**
- personal, home, family, health
- grocery, doctor, dentist, appointment
- exercise, gym, vacation
- birthday, anniversary, hobby

**Business Keywords:**
- business, client, customer, invoice
- payment, project, meeting, proposal
- linkedin, twitter, facebook, instagram
- accounting, odoo, ceo, briefing

### Cross-Domain Detection

Tasks with significant keywords from both domains are classified as cross-domain:
- Requires 2+ personal keywords AND 2+ business keywords
- Example: "Schedule business meeting and pick up kids from school"

### Linked Tasks

When a cross-domain task is processed:
1. Creates a task in Personal/Needs_Action
2. Creates a task in Business/Needs_Action
3. Both tasks reference each other
4. Original task archived in Cross_Domain/Archive

### Unified Reporting

The unified report shows:
- Task counts by domain
- Task status (inbox, needs_action, done)
- Work-life balance percentages
- Total tasks across all domains

## Integration

### Scheduler Integration

Add to `scripts/scheduler.py`:

```python
# Process cross-domain tasks every hour
scheduler.add_task(
    name="process_cross_domain",
    interval_seconds=3600,  # Hourly
    command="scripts/cross_domain_router.py",
    args=["process-cross-domain"]
)

# Generate unified report daily
scheduler.add_task(
    name="unified_report",
    interval_seconds=86400,  # Daily
    command="scripts/cross_domain_router.py",
    args=["unified-report"]
)
```

### CEO Briefing Integration

The unified report can be included in CEO briefings to show work-life balance.

### Logging

All cross-domain operations are logged to:
- `AI_Employee_Vault/Logs/routing.log` - Task routing history
- `AI_Employee_Vault/Logs/business.log` - Cross-domain activity
- `AI_Employee_Vault/Logs/error.log` - Errors

## Use Cases

### Example 1: Business Meeting with Personal Impact

Task: "Schedule client meeting on Friday and arrange childcare"

**Classification:** Cross-domain

**Result:**
- Business task: "Schedule client meeting on Friday"
- Personal task: "Arrange childcare for Friday"
- Both tasks linked

### Example 2: Pure Business Task

Task: "Send invoice to Client A for January services"

**Classification:** Business

**Result:**
- Routed to Business/Inbox
- No personal task created

### Example 3: Pure Personal Task

Task: "Buy groceries: milk, eggs, bread"

**Classification:** Personal

**Result:**
- Routed to Personal/Inbox
- No business task created

## Work-Life Balance Tracking

The unified report includes work-life balance metrics:

```
Work-Life Balance:
- Business Tasks: 20 (64.5%)
- Personal Tasks: 11 (35.5%)
- Cross-Domain: 1 (3.2%)
```

This helps you:
- Monitor if you're overworking
- Ensure personal tasks get attention
- Balance business and personal priorities

## Examples

### Example 1: Route a Task

```bash
# Task file contains: "Schedule dentist appointment"
python scripts/cross_domain_router.py route "AI_Employee_Vault/Inbox/task.md"

# Output:
{
  "success": true,
  "task": "task.md",
  "source": null,
  "destination": "personal",
  "classification": "personal"
}
```

### Example 2: Process Cross-Domain Tasks

```bash
python scripts/cross_domain_router.py process-cross-domain

# Output:
{
  "success": true,
  "message": "Processed 1 cross-domain tasks",
  "processed": 1,
  "results": [
    {
      "original": "meeting_and_childcare.md",
      "personal_task": "20260224_091400_cross_domain_personal_meeting_and_childcare.md",
      "business_task": "20260224_091400_cross_domain_business_meeting_and_childcare.md"
    }
  ]
}
```

### Example 3: Generate Unified Report

```bash
python scripts/cross_domain_router.py unified-report

# Creates: AI_Employee_Vault/Reports/Unified_Report.md
```

## Security

- All data stored locally
- No external API calls
- Complete audit trail in routing.log
- Privacy maintained across domains

## Files

- **Script:** `scripts/cross_domain_router.py`
- **Unified Report:** `AI_Employee_Vault/Reports/Unified_Report.md`
- **Routing Log:** `AI_Employee_Vault/Logs/routing.log`
- **Business Log:** `AI_Employee_Vault/Logs/business.log`
- **Error Log:** `AI_Employee_Vault/Logs/error.log`

## API Reference

### route_task(task_file, source_domain)

Routes a task to the appropriate domain.

**Parameters:**
- `task_file` (Path): Path to task file
- `source_domain` (string, optional): Source domain

**Returns:** Routing result or error

### process_cross_domain_tasks()

Processes all tasks in Cross_Domain folder.

**Returns:** Processing results or error

### generate_unified_report()

Generates unified report across all domains.

**Returns:** Report data or error

## Future Enhancements

- Automatic task splitting (one task → multiple domain tasks)
- Smart scheduling (coordinate personal and business calendars)
- Priority balancing (ensure personal tasks don't get neglected)
- Time tracking across domains
- Dependency management (business task depends on personal task)

## Status

✅ **Production Ready**
- Cross-domain task routing
- Linked task creation
- Unified reporting
- Work-life balance tracking
- Complete logging

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Operational ✅
