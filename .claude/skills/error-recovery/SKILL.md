# Error Recovery Agent Skill

## Overview

The Error Recovery skill provides automatic error handling, logging, and retry mechanisms for failed tasks. It ensures system resilience by capturing errors, moving failed tasks to a dedicated folder, and attempting automatic recovery.

## Capabilities

1. **Error Logging**
   - Log all errors to logs/error.log
   - Structured error format with timestamps
   - Stack traces and context information
   - Error categorization

2. **Failed Task Management**
   - Move failed tasks to AI_Employee_Vault/Errors/
   - Preserve original task information
   - Add error metadata to task file
   - Track retry attempts

3. **Automatic Retry**
   - Retry failed tasks once after 5 minutes
   - Exponential backoff for multiple failures
   - Maximum retry limit (default: 3 attempts)
   - Skip retry for permanent failures

4. **Error Monitoring**
   - Track error rates
   - Generate error reports
   - Alert on critical errors
   - System health metrics

## Usage

### Automatic Error Handling

The error recovery system runs automatically when any task fails. No manual intervention required.

### Manual Operations

```bash
# Check error log
python scripts/error_recovery.py check

# Retry all failed tasks
python scripts/error_recovery.py retry-all

# Retry specific task
python scripts/error_recovery.py retry --task-id TASK_ID

# Generate error report
python scripts/error_recovery.py report

# Clear resolved errors
python scripts/error_recovery.py clear-resolved
```

### Trigger Phrases

When the user says any of these, invoke this skill:

- "Check for errors"
- "Show error log"
- "Retry failed tasks"
- "What went wrong?"
- "System errors"
- "Error report"
- "Fix failed tasks"
- "Recover from errors"

## Error Log Format

### error.log Structure

```
[2026-02-23 17:05:00] ERROR | Task: task_123.md | Type: EmailSendError | Message: SMTP connection timeout
[2026-02-23 17:05:00] STACK | File: scripts/send_email.py, Line: 45, Function: send_email_sync
[2026-02-23 17:05:00] CONTEXT | Recipient: client@example.com, Subject: Invoice #1234
[2026-02-23 17:05:00] RETRY | Attempt 1/3 scheduled for 2026-02-23 17:10:00
---
[2026-02-23 17:10:00] RETRY | Task: task_123.md | Attempt: 1/3
[2026-02-23 17:10:00] SUCCESS | Task recovered successfully
---
```

## Failed Task File Format

When a task fails, it's moved to `AI_Employee_Vault/Errors/` with metadata:

```markdown
---
original_location: AI_Employee_Vault/Needs_Action/task_123.md
error_timestamp: 2026-02-23T17:05:00Z
error_type: EmailSendError
error_message: SMTP connection timeout
retry_count: 1
max_retries: 3
next_retry: 2026-02-23T17:10:00Z
status: pending_retry
---

# Original Task Content

[Original task content preserved here]

---

## Error Details

**Error Type**: EmailSendError
**Error Message**: SMTP connection timeout
**Timestamp**: 2026-02-23 17:05:00
**Stack Trace**:
```
File: scripts/send_email.py, Line: 45, Function: send_email_sync
Error: Connection to smtp.gmail.com timed out after 30 seconds
```

**Context**:
- Recipient: client@example.com
- Subject: Invoice #1234
- Attempt: 1/3

## Recovery Actions

- [x] Error logged to logs/error.log
- [x] Task moved to Errors folder
- [ ] Retry scheduled for 2026-02-23 17:10:00
- [ ] Manual intervention required if retry fails

---
*Error captured by Error Recovery System*
```

## Workflow

### 1. Error Detection

When any script or operation fails:

1. Exception is caught by error handler
2. Error details are extracted
3. Error is logged to error.log
4. Task file is moved to Errors folder
5. Retry is scheduled

### 2. Error Logging

```python
# Automatic error logging
try:
    # Task execution
    result = execute_task(task)
except Exception as e:
    error_recovery.log_error(
        task_id="task_123.md",
        error_type=type(e).__name__,
        error_message=str(e),
        stack_trace=traceback.format_exc(),
        context={"recipient": "client@example.com"}
    )
```

### 3. Task Movement

Failed task is moved from original location to Errors folder:

```
AI_Employee_Vault/Needs_Action/task_123.md
    ↓
AI_Employee_Vault/Errors/task_123_ERROR_20260223_170500.md
```

### 4. Retry Mechanism

After 5 minutes (configurable):

1. Error recovery system checks for pending retries
2. Task is moved back to original location
3. Task is re-executed
4. If successful: moved to Done
5. If failed: retry count incremented, moved back to Errors

### 5. Maximum Retries

After 3 failed attempts (configurable):

1. Task is marked as "permanent_failure"
2. Human notification is triggered
3. Task remains in Errors folder
4. Manual intervention required

## Error Categories

### Transient Errors (Retry Automatically)
- Network timeouts
- API rate limits
- Temporary service unavailability
- Connection errors

### Permanent Errors (No Retry)
- Invalid credentials
- File not found
- Permission denied
- Invalid data format

### Critical Errors (Immediate Alert)
- System crashes
- Data corruption
- Security violations
- Resource exhaustion

## Configuration

Set these environment variables:

```bash
# Retry delay in seconds (default: 300 = 5 minutes)
export ERROR_RETRY_DELAY=300

# Maximum retry attempts (default: 3)
export ERROR_MAX_RETRIES=3

# Enable exponential backoff (default: true)
export ERROR_EXPONENTIAL_BACKOFF=true

# Alert email for critical errors
export ERROR_ALERT_EMAIL="admin@example.com"

# Error log rotation size in MB (default: 10)
export ERROR_LOG_MAX_SIZE=10
```

## Integration Points

### With Other Skills

- **vault-file-manager**: Move failed tasks to Errors folder
- **gmail-send**: Send error alerts via email
- **human-approval**: Request manual intervention for permanent failures
- **ceo-briefing**: Include error summary in weekly report

### With MCP Server

- **log_activity**: Log all errors to business.log
- **send_email**: Email critical error alerts

### With Scheduler

```python
# Check for pending retries every minute
schedule.every(1).minutes.do(
    lambda: subprocess.run([
        "python", "scripts/error_recovery.py", "check-retries"
    ])
)

# Generate daily error report
schedule.every().day.at("08:00").do(
    lambda: subprocess.run([
        "python", "scripts/error_recovery.py", "report", "--period", "daily"
    ])
)
```

## Examples

### Example 1: Email Send Failure

**Scenario**: Email fails due to network timeout

```bash
# Automatic handling:
1. Error logged to logs/error.log
2. Task moved to AI_Employee_Vault/Errors/
3. Retry scheduled for 5 minutes later
4. After 5 minutes, task is retried
5. If successful, moved to Done
```

### Example 2: LinkedIn Post Failure

**Scenario**: LinkedIn automation fails due to changed UI

```bash
# Automatic handling:
1. Error logged with screenshot
2. Task moved to Errors folder
3. Retry attempted once
4. After failure, marked as permanent_failure
5. Human notification sent
```

### Example 3: Check Error Status

```bash
python scripts/error_recovery.py check
```

**Output:**
```json
{
  "success": true,
  "total_errors": 5,
  "pending_retry": 2,
  "permanent_failures": 1,
  "resolved": 2,
  "recent_errors": [
    {
      "task": "task_123.md",
      "error": "EmailSendError",
      "timestamp": "2026-02-23 17:05:00",
      "status": "pending_retry",
      "next_retry": "2026-02-23 17:10:00"
    }
  ]
}
```

### Example 4: Generate Error Report

```bash
python scripts/error_recovery.py report --period week
```

**Output:**
```json
{
  "success": true,
  "period": "Week of Feb 17-23, 2026",
  "total_errors": 12,
  "error_rate": "2.3%",
  "most_common_errors": [
    {"type": "EmailSendError", "count": 5},
    {"type": "LinkedInTimeoutError", "count": 3},
    {"type": "FileNotFoundError", "count": 2}
  ],
  "recovery_rate": "83.3%",
  "permanent_failures": 2
}
```

## Error Recovery Strategies

### Strategy 1: Exponential Backoff

For transient errors, use exponential backoff:

- Attempt 1: Wait 5 minutes
- Attempt 2: Wait 10 minutes
- Attempt 3: Wait 20 minutes

### Strategy 2: Circuit Breaker

If error rate exceeds threshold:

1. Pause all operations for 5 minutes
2. Log circuit breaker activation
3. Send alert to admin
4. Resume operations after cooldown

### Strategy 3: Graceful Degradation

If critical service fails:

1. Continue with reduced functionality
2. Queue operations for later
3. Notify user of degraded mode
4. Attempt recovery in background

## Monitoring and Alerts

### Error Rate Monitoring

```bash
# Check error rate
python scripts/error_recovery.py metrics
```

**Output:**
```json
{
  "error_rate_1h": "1.2%",
  "error_rate_24h": "2.3%",
  "error_rate_7d": "1.8%",
  "trend": "stable",
  "alert_threshold": "5.0%",
  "status": "healthy"
}
```

### Critical Error Alerts

When critical errors occur:

1. Email sent to ERROR_ALERT_EMAIL
2. Entry added to business.log
3. Task moved to Errors folder with high priority
4. System health status updated

## Best Practices

1. **Log Everything** - Capture full context for debugging
2. **Preserve Original Data** - Never lose task information
3. **Retry Intelligently** - Use exponential backoff
4. **Alert Appropriately** - Don't spam, but don't miss critical issues
5. **Monitor Trends** - Track error rates over time
6. **Clean Up** - Archive resolved errors regularly

## Troubleshooting

### Issue: Errors not being logged

**Solution:** Check error.log permissions
```bash
ls -la AI_Employee_Vault/Logs/error.log
chmod 644 AI_Employee_Vault/Logs/error.log
```

### Issue: Retries not executing

**Solution:** Check scheduler is running
```bash
ps aux | grep scheduler.py
python scripts/scheduler.py &
```

### Issue: Too many errors

**Solution:** Check system health
```bash
python scripts/error_recovery.py report
python scripts/ceo_briefing.py generate
```

## Gold Tier Requirement

This skill fulfills Gold Tier requirement #8:
- Error recovery and graceful degradation

The system provides:
- Automatic error detection and logging
- Intelligent retry mechanisms
- Graceful degradation strategies
- Comprehensive error monitoring
- Human-in-the-loop for permanent failures

## Future Enhancements

- AI-powered error analysis
- Predictive failure detection
- Automatic root cause analysis
- Self-healing capabilities
- Error pattern recognition
- Integration with monitoring tools

---

**Skill Type:** Agent Skill (Automated)
**Dependencies:** Python 3.13+, scripts/error_recovery.py
**Schedule:** Check retries every minute
**Security Level:** High (system stability)
**Approval Required:** No (automatic recovery)
