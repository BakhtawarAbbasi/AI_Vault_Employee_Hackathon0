# Ralph Wiggum Autonomous Loop Agent Skill

## Overview

The Ralph Wiggum Autonomous Loop provides continuous, multi-step task execution without human intervention. It analyzes tasks, creates plans, executes steps iteratively, and continues until completion or maximum iterations are reached.

## Capabilities

1. **Autonomous Task Execution**
   - Analyze incoming tasks automatically
   - Create detailed execution plans
   - Execute steps iteratively
   - Check results after each step
   - Continue until task completion

2. **Iterative Processing**
   - Maximum 5 iterations per task (configurable)
   - Check completion status after each iteration
   - Automatic progression through plan steps
   - Result validation between steps

3. **Safety Mechanisms**
   - Maximum iteration limit (default: 5)
   - Human approval for risky operations
   - Automatic failure detection
   - Graceful degradation on errors

4. **Integration**
   - Works with existing task system
   - Integrates with scheduler
   - Uses error recovery system
   - Logs all activities

## Usage

### Automatic Execution

The Ralph Wiggum loop runs automatically when tasks appear in the Inbox:

1. Task detected in Inbox
2. Loop analyzes task
3. Creates Plan.md
4. Executes first step
5. Checks result
6. Continues to next step
7. Repeats until completed or max iterations
8. Moves task to Done

### Manual Execution

```bash
# Process specific task
python scripts/ralph_wiggum.py process --task-file AI_Employee_Vault/Inbox/task.md

# Process all tasks in Inbox
python scripts/ralph_wiggum.py process-all

# Check loop status
python scripts/ralph_wiggum.py status

# Stop running loop
python scripts/ralph_wiggum.py stop --task-id task_123
```

### Trigger Phrases

When the user says any of these, invoke this skill:

- "Process this task autonomously"
- "Run Ralph Wiggum loop"
- "Execute task automatically"
- "Complete this task end-to-end"
- "Autonomous execution"
- "Run until complete"
- "Auto-process task"

## Workflow

### 1. Task Detection

When a new task appears in Inbox:

```
AI_Employee_Vault/Inbox/new_task.md
    ↓
Ralph Wiggum Loop activated
```

### 2. Task Analysis

```python
# Analyze task content
task_analysis = {
    'title': 'Send invoice to Client A',
    'complexity': 'medium',
    'steps_required': 3,
    'risky': False,
    'estimated_iterations': 2
}
```

### 3. Plan Creation

Create detailed Plan.md:

```markdown
# Task Plan: Send invoice to Client A

## Steps
1. [ ] Generate invoice PDF
2. [ ] Compose email with invoice
3. [ ] Send email to client

## Iteration Limit: 5
## Current Iteration: 0
## Status: pending
```

### 4. Iterative Execution

```
Iteration 1:
  - Execute Step 1: Generate invoice PDF
  - Check result: ✓ Success
  - Update plan: Step 1 complete

Iteration 2:
  - Execute Step 2: Compose email
  - Check result: ✓ Success
  - Update plan: Step 2 complete

Iteration 3:
  - Execute Step 3: Send email
  - Check result: ✓ Success
  - Update plan: Step 3 complete
  - Task complete!

Move to Done folder
```

### 5. Completion Check

After each iteration:

```python
def is_task_complete(plan):
    # Check if all steps are completed
    all_steps_done = all(step['completed'] for step in plan['steps'])

    # Check if task file moved to Done
    task_in_done = os.path.exists(f"AI_Employee_Vault/Done/{task_id}")

    return all_steps_done or task_in_done
```

## Plan.md Format

```markdown
---
task_id: task_123.md
original_location: AI_Employee_Vault/Inbox/task_123.md
created: 2026-02-23T17:07:00Z
max_iterations: 5
current_iteration: 0
status: in_progress
risky: false
---

# Task Plan: Send Invoice to Client A

## Objective
Send invoice #1234 to Client A via email

## Steps

### Step 1: Generate Invoice PDF
- [ ] Status: pending
- Action: Run invoice generator
- Expected output: invoice_1234.pdf
- Validation: File exists and is valid PDF

### Step 2: Compose Email
- [ ] Status: pending
- Action: Create email with invoice attachment
- Expected output: Email draft ready
- Validation: Email has recipient, subject, body, attachment

### Step 3: Send Email
- [ ] Status: pending
- Action: Send email via SMTP
- Expected output: Email sent successfully
- Validation: SMTP returns success code
- **Requires approval**: Yes (external communication)

## Iteration Log

### Iteration 1 (2026-02-23 17:07:15)
- Executed: Step 1
- Result: Success
- Output: invoice_1234.pdf created
- Next: Step 2

### Iteration 2 (2026-02-23 17:08:30)
- Executed: Step 2
- Result: Success
- Output: Email draft created
- Next: Step 3 (requires approval)

### Iteration 3 (2026-02-23 17:10:45)
- Executed: Step 3
- Result: Success
- Output: Email sent to client@example.com
- Task: COMPLETE

## Completion Status
- [x] All steps completed
- [x] Task moved to Done
- [x] Execution log saved

---
*Completed by Ralph Wiggum Autonomous Loop*
*Total iterations: 3/5*
*Duration: 3 minutes 30 seconds*
```

## Safety Mechanisms

### 1. Maximum Iterations

```python
MAX_ITERATIONS = int(os.getenv('RALPH_MAX_ITERATIONS', '5'))

if current_iteration >= MAX_ITERATIONS:
    log_error("Max iterations reached")
    move_to_errors(task, "MaxIterationsExceeded")
    send_alert("Task exceeded max iterations")
```

### 2. Risky Operation Detection

```python
RISKY_KEYWORDS = [
    'delete', 'remove', 'drop', 'truncate',
    'payment', 'transfer', 'send money',
    'publish', 'post', 'tweet', 'share'
]

def is_risky(task_content):
    content_lower = task_content.lower()
    return any(keyword in content_lower for keyword in RISKY_KEYWORDS)
```

### 3. Human Approval for Risky Operations

```python
if is_risky(task) or step.requires_approval:
    # Create approval request
    approval_file = create_approval_request(task, step)

    # Wait for approval
    while not is_approved(approval_file):
        time.sleep(10)  # Check every 10 seconds

        # Timeout after 1 hour
        if time_elapsed > 3600:
            move_to_needs_approval(task)
            return "awaiting_approval"

    # Continue execution after approval
    execute_step(step)
```

### 4. Error Handling

```python
try:
    result = execute_step(step)
except Exception as e:
    # Log error
    error_recovery.log_error(task_id, type(e).__name__, str(e))

    # Move to errors folder
    error_recovery.move_to_errors(task_file, type(e).__name__, str(e))

    # Stop loop
    return "error"
```

## Configuration

Set these environment variables:

```bash
# Maximum iterations per task (default: 5)
export RALPH_MAX_ITERATIONS=5

# Iteration delay in seconds (default: 10)
export RALPH_ITERATION_DELAY=10

# Enable human approval for risky operations (default: true)
export RALPH_REQUIRE_APPROVAL=true

# Timeout for approval in seconds (default: 3600 = 1 hour)
export RALPH_APPROVAL_TIMEOUT=3600

# Enable verbose logging (default: false)
export RALPH_VERBOSE=false
```

## Integration with Scheduler

Add to `scripts/scheduler.py`:

```python
# Task 6: Ralph Wiggum autonomous loop - check every 30 seconds
scheduler.add_task(
    name="ralph_wiggum_loop",
    interval_seconds=30,  # Check every 30 seconds
    command="scripts/ralph_wiggum.py",
    args=["process-all"]
)
```

## Examples

### Example 1: Simple Task (No Approval Needed)

**Task**: Create a summary report

```markdown
# Create Summary Report

Generate a summary of this week's activities and save to Reports folder.
```

**Execution**:
```
Iteration 1: Analyze task → Create plan
Iteration 2: Gather data from Done folder
Iteration 3: Generate summary markdown
Iteration 4: Save to Reports folder
Task complete! (4/5 iterations)
```

### Example 2: Risky Task (Approval Required)

**Task**: Send payment to vendor

```markdown
# Send Payment to Vendor X

Transfer $1,500 to Vendor X for services rendered.
```

**Execution**:
```
Iteration 1: Analyze task → Detected as RISKY
Iteration 2: Create approval request
Status: Awaiting human approval
[User approves]
Iteration 3: Execute payment
Task complete! (3/5 iterations)
```

### Example 3: Complex Multi-Step Task

**Task**: Complete client onboarding

```markdown
# Client Onboarding - Acme Corp

1. Send welcome email
2. Create project folder
3. Generate contract
4. Schedule kickoff meeting
5. Send calendar invite
```

**Execution**:
```
Iteration 1: Analyze task → Create 5-step plan
Iteration 2: Send welcome email → Success
Iteration 3: Create project folder → Success
Iteration 4: Generate contract → Success
Iteration 5: Schedule meeting + send invite → Success
Task complete! (5/5 iterations - max reached)
```

### Example 4: Task with Error

**Task**: Send email to invalid address

```markdown
# Send Email

Send project update to client@invalid-domain-xyz.com
```

**Execution**:
```
Iteration 1: Analyze task → Create plan
Iteration 2: Compose email → Success
Iteration 3: Send email → ERROR (Invalid recipient)
Error logged to error.log
Task moved to Errors folder
Retry scheduled for 5 minutes
```

## Loop State Management

### State File Format

```json
{
  "task_123.md": {
    "status": "in_progress",
    "current_iteration": 2,
    "max_iterations": 5,
    "started_at": "2026-02-23T17:07:00Z",
    "last_iteration": "2026-02-23T17:08:30Z",
    "steps_completed": 2,
    "steps_total": 4,
    "awaiting_approval": false,
    "risky": false
  }
}
```

### State Transitions

```
pending → in_progress → completed
                     → error
                     → awaiting_approval → in_progress
                     → max_iterations_exceeded
```

## Monitoring

### Check Loop Status

```bash
python scripts/ralph_wiggum.py status
```

**Output**:
```json
{
  "success": true,
  "active_loops": 2,
  "tasks": [
    {
      "task_id": "task_123.md",
      "status": "in_progress",
      "iteration": "2/5",
      "steps_completed": "2/4",
      "started": "2 minutes ago"
    },
    {
      "task_id": "task_456.md",
      "status": "awaiting_approval",
      "iteration": "3/5",
      "steps_completed": "2/3",
      "started": "10 minutes ago"
    }
  ]
}
```

## Performance Metrics

Track loop performance:

```python
metrics = {
    'total_tasks_processed': 45,
    'average_iterations': 2.8,
    'success_rate': '93.3%',
    'average_duration': '4 minutes 15 seconds',
    'tasks_requiring_approval': 8,
    'tasks_with_errors': 3
}
```

## Best Practices

1. **Keep Tasks Focused** - One clear objective per task
2. **Use Clear Language** - Explicit instructions work best
3. **Mark Risky Operations** - Use keywords like "payment", "delete"
4. **Monitor Progress** - Check status regularly
5. **Set Realistic Limits** - Adjust max iterations based on task complexity
6. **Review Logs** - Check iteration logs for optimization

## Troubleshooting

### Issue: Loop stuck in infinite iteration

**Solution**: Check max iterations setting
```bash
export RALPH_MAX_ITERATIONS=5
python scripts/ralph_wiggum.py stop --task-id task_123
```

### Issue: Task not completing

**Solution**: Check plan and iteration log
```bash
cat AI_Employee_Vault/Needs_Action/Plan_task_123.md
```

### Issue: Too many approval requests

**Solution**: Adjust risky keyword detection
```python
# Edit RISKY_KEYWORDS in ralph_wiggum.py
```

## Gold Tier Requirement

This skill fulfills Gold Tier requirement #10:
- Ralph Wiggum loop for autonomous multi-step task completion

The system provides:
- Continuous task execution without human intervention
- Iterative step-by-step processing
- Automatic completion detection
- Safety mechanisms (max iterations, approval for risky ops)
- Error handling and recovery
- Complete audit trail

## Future Enhancements

- AI-powered step generation
- Dynamic iteration limit adjustment
- Parallel task execution
- Learning from past executions
- Predictive completion time
- Advanced risk detection

---

**Skill Type:** Agent Skill (Autonomous)
**Dependencies:** Python 3.13+, scripts/ralph_wiggum.py
**Schedule:** Check every 30 seconds
**Security Level:** High (autonomous execution)
**Approval Required:** Yes (for risky operations)
