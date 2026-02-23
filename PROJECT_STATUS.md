# Personal AI Employee - Project Status

## Project Overview

This is a Personal AI Employee system built for the Panaversity Hackathon 0. It implements a local-first, agent-driven, human-in-the-loop autonomous system that manages personal and business tasks 24/7.

## Current Status: Silver Tier Complete ✓

### Bronze Tier (COMPLETE)
- ✓ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✓ Working file system watcher (scripts/watcher_comprehensive.py)
- ✓ Claude Code reading/writing to vault
- ✓ Folder structure: /Inbox, /Needs_Action, /Done, /Needs_Approval
- ✓ All AI functionality implemented as Agent Skills

### Silver Tier (COMPLETE)
- ✓ All Bronze requirements
- ✓ Multiple Watcher scripts (watcher_comprehensive.py, watcher_linkedin.py)
- ✓ LinkedIn posting capability (via business-mcp server)
- ✓ Claude reasoning loop creating Plan.md files (scripts/create_task_plan.py)
- ✓ Working MCP server for external actions (mcp/business_mcp/)
- ✓ Human-in-the-loop approval workflow (scripts/request_approval.py)
- ✓ Basic scheduling (scripts/scheduler.py)
- ✓ All AI functionality as Agent Skills (7 skills total)

## Architecture

```
AI_Employee_Vault/          # Unified vault for all operations
├── Inbox/                  # New tasks arrive here
├── Needs_Action/           # Tasks requiring processing
├── Done/                   # Completed tasks
├── Needs_Approval/         # Tasks awaiting human approval
└── Logs/                   # System and business logs

scripts/                    # Core functionality
├── create_task_plan.py     # Reasoning workflow (Silver Tier)
├── watcher_comprehensive.py # File system watcher
├── watcher_linkedin.py     # LinkedIn monitoring
├── scheduler.py            # Task scheduling
├── send_email.py           # Email capability
├── post_linkedin.py        # LinkedIn posting
├── move_task.py            # Vault file manager
└── request_approval.py     # HITL workflow

.claude/skills/             # Agent Skills (7 total)
├── gmail-send/
├── linkedin-post/
├── vault-file-manager/
├── human-approval/
├── task-planner/
├── linkedin-watcher/
└── file-triage/

mcp/business_mcp/           # MCP Server (NEW)
├── server.py               # Main MCP implementation
├── README.md               # Documentation
├── QUICKSTART.md           # Quick start guide
├── requirements.txt        # Dependencies
├── test_server.py          # Test suite
└── VERIFICATION.md         # Silver Tier verification
```

## Key Features

### 1. Reasoning Workflows
- Automatic Plan.md generation from tasks
- Structured planning with objectives and steps
- Priority assessment and approval requirements

### 2. Multiple Watchers
- **File System Watcher**: Monitors Inbox for new .md files
- **LinkedIn Watcher**: Monitors for business opportunities
- **Scheduler**: Runs recurring tasks

### 3. MCP Server (Business Actions)
- **send_email**: Send emails via SMTP (Gmail)
- **post_linkedin**: Create LinkedIn posts via browser automation
- **log_activity**: Log business activities to vault

### 4. Human-in-the-Loop
- Approval workflow for sensitive actions
- Files moved to Needs_Approval folder
- User reviews and approves/rejects
- System executes only after approval

### 5. Agent Skills
- 7 production-ready skills replacing MCP functionality
- Local execution with environment variable security
- JSON output format for all operations

## Technology Stack

- **Brain**: Claude Code (reasoning engine)
- **Memory/GUI**: Obsidian vault (local markdown)
- **Watchers**: Python scripts with watchdog library
- **Automation**: Playwright for browser automation
- **Email**: SMTP via smtplib
- **MCP**: Python-based MCP server
- **Security**: Environment variables for credentials

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r mcp/business_mcp/requirements.txt
playwright install chromium
```

### 2. Set Environment Variables
```bash
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export LINKEDIN_EMAIL="your-linkedin@email.com"
export LINKEDIN_PASSWORD="your-linkedin-password"
```

### 3. Run Silver Tier Demo
```bash
python run_silver_tier.py
```

### 4. Start Watchers
```bash
# Terminal 1: File system watcher
python scripts/watcher_comprehensive.py

# Terminal 2: LinkedIn watcher
python scripts/watcher_linkedin.py

# Terminal 3: Scheduler
python scripts/scheduler.py
```

### 5. Configure MCP Server
Add to Claude Desktop config (`~/.claude/config.json`):
```json
{
  "mcpServers": {
    "business-mcp": {
      "command": "python",
      "args": ["D:\\personal-ai-employee-hackathon\\mcp\\business_mcp\\server.py"],
      "env": {
        "EMAIL_ADDRESS": "your-email@gmail.com",
        "EMAIL_PASSWORD": "your-app-password",
        "LINKEDIN_EMAIL": "your-linkedin@email.com",
        "LINKEDIN_PASSWORD": "your-linkedin-password"
      }
    }
  }
}
```

## Testing

### Test MCP Server
```bash
python mcp/business_mcp/test_server.py
```

### Test Individual Components
```bash
# Test email sending
python scripts/send_email.py "test@example.com" "Test Subject" "Test body"

# Test task planning
python scripts/create_task_plan.py

# Test file moving
python scripts/move_task.py Inbox Done sample_task.md
```

## Usage Examples

### 1. Create a Task
Drop a markdown file in `AI_Employee_Vault/Inbox/`:
```markdown
# Client Follow-up

## Description
Follow up with Client A about project proposal

## Details
- Client: Client A
- Topic: Project proposal review
- Deadline: End of week
```

### 2. System Processes Task
- Watcher detects new file
- Creates action file in Needs_Action
- Reasoning workflow creates Plan.md
- Plan includes steps and approval requirements

### 3. Execute Actions
- Use MCP server to send emails
- Post LinkedIn updates
- Log all activities
- Move completed tasks to Done

## Security

- ✓ Environment variables for credentials
- ✓ No hardcoded secrets
- ✓ Human-in-the-loop for sensitive actions
- ✓ Audit logging for all operations
- ✓ Local-first architecture

## Documentation

- `projectrequirment.md` - Hackathon requirements
- `mcp/business_mcp/README.md` - MCP server documentation
- `mcp/business_mcp/QUICKSTART.md` - Quick start guide
- `mcp/business_mcp/VERIFICATION.md` - Silver Tier verification
- `.claude/skills/*/SKILL.md` - Individual skill documentation

## Next Steps (Gold Tier)

To achieve Gold Tier, implement:
- [ ] Full cross-domain integration (Personal + Business)
- [ ] Odoo Community accounting system integration
- [ ] Facebook and Instagram integration
- [ ] Twitter (X) integration
- [ ] Weekly Business Audit with CEO Briefing
- [ ] Error recovery and graceful degradation
- [ ] Comprehensive audit logging
- [ ] Ralph Wiggum loop for autonomous task completion
- [ ] Architecture documentation

## Submission

- **Tier**: Silver Tier (Complete)
- **Repository**: D:\personal-ai-employee-hackathon
- **Demo**: Run `python run_silver_tier.py`
- **Security**: Environment variables for all credentials
- **Documentation**: Complete with README, QUICKSTART, and VERIFICATION

## Contact

For questions or issues, refer to the Panaversity Hackathon 0 documentation or join the Wednesday Research Meetings.

---

**Last Updated**: 2026-02-23
**Status**: Silver Tier Complete ✓
**Next Goal**: Gold Tier Implementation
