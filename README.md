# Personal AI Employee - Hackathon Project

> A local-first, agent-driven, human-in-the-loop autonomous system that manages personal and business tasks 24/7.

Built for **Panaversity Hackathon 0: Building Autonomous FTEs (Full-Time Equivalent) in 2026**

## 🏆 Project Status

- ✅ **Bronze Tier**: Complete
- ✅ **Silver Tier**: Complete
- 🚧 **Gold Tier**: In Progress (2/12 requirements)

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 24+ LTS
- Git
- Obsidian (optional, for GUI)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd personal-ai-employee-hackathon

# Install Python dependencies
pip install -r requirements.txt
pip install -r mcp/business_mcp/requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Configuration

Set environment variables:

```bash
# Email configuration
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"

# LinkedIn configuration
export LINKEDIN_EMAIL="your-linkedin@email.com"
export LINKEDIN_PASSWORD="your-linkedin-password"

# CEO briefing email
export CEO_EMAIL="your-email@example.com"

# Accounting threshold
export ACCOUNTING_APPROVAL_THRESHOLD=500
```

### Run the System

```bash
# Demo Silver Tier functionality
python run_silver_tier.py

# Start file system watcher
python scripts/watcher_comprehensive.py

# Start scheduler (includes CEO briefing)
python scripts/scheduler.py
```

## 📁 Project Structure

```
AI_Employee_Vault/          # Main vault (Obsidian-compatible)
├── Inbox/                  # Drop tasks here
├── Needs_Action/           # Tasks being processed
├── Done/                   # Completed tasks
├── Needs_Approval/         # Awaiting human approval
├── Accounting/             # Financial records
│   └── Current_Month.md    # Current transactions
├── Reports/                # Executive reports
│   └── CEO_Weekly.md       # Weekly CEO briefing
└── Logs/                   # Activity logs

scripts/                    # Core functionality
├── accounting_manager.py   # Financial tracking
├── ceo_briefing.py         # Executive summaries
├── create_task_plan.py     # Task planning
├── scheduler.py            # Task scheduling
└── ...                     # Other utilities

.claude/skills/             # 9 Agent Skills
├── accounting-manager/
├── ceo-briefing/
├── gmail-send/
├── linkedin-post/
└── ...

mcp/business_mcp/           # MCP Server
└── server.py               # Business actions
```

## 🎯 Key Features

### 1. Financial Tracking
Track income and expenses with automatic summaries:

```bash
# Log income
python scripts/accounting_manager.py log --type income --amount 250 --description "Client payment"

# Show totals
python scripts/accounting_manager.py totals

# Weekly summary
python scripts/accounting_manager.py summary --period week
```

### 2. CEO Briefing
Automatic weekly executive summaries:

```bash
# Generate briefing
python scripts/ceo_briefing.py generate

# View latest
python scripts/ceo_briefing.py view

# Email briefing
python scripts/ceo_briefing.py email --to ceo@example.com
```

### 3. Task Management
Automated task processing with reasoning:

- Drop `.md` files in `AI_Employee_Vault/Inbox/`
- System creates Plan.md files automatically
- Tasks move through workflow: Inbox → Needs_Action → Done

### 4. Business Actions (MCP Server)
- Send emails via SMTP
- Create LinkedIn posts
- Log business activities

### 5. Human-in-the-Loop
- Approval required for transactions over $500
- Sensitive actions require manual approval
- All actions logged for audit trail

## 🛠️ Agent Skills (9 Total)

1. **accounting-manager** - Financial tracking and reporting
2. **ceo-briefing** - Weekly executive summaries
3. **gmail-send** - Email sending via SMTP
4. **linkedin-post** - LinkedIn post creation
5. **vault-file-manager** - File organization
6. **human-approval** - Approval workflows
7. **task-planner** - Task planning and reasoning
8. **linkedin-watcher** - LinkedIn monitoring
9. **file-triage** - Inbox processing

## 📊 Achievements

### Silver Tier (Complete)
- ✅ Multiple watchers (file system, LinkedIn)
- ✅ Reasoning workflows (Plan.md generation)
- ✅ MCP server (business actions)
- ✅ Human-in-the-loop approval
- ✅ Scheduling system
- ✅ 9 Agent Skills

### Gold Tier (In Progress)
- ✅ Weekly Business Audit with CEO Briefing
- ✅ Comprehensive audit logging
- ⏳ Odoo accounting integration
- ⏳ Social media integrations (Facebook, Instagram, Twitter)
- ⏳ Error recovery and graceful degradation
- ⏳ Ralph Wiggum autonomous loop

## 🔒 Security

- Environment variables for all credentials
- No hardcoded secrets
- Human approval for sensitive actions
- Complete audit trail in business.log
- Local-first architecture
- Approval thresholds for financial transactions

## 📖 Documentation

- **FINAL_SUMMARY.md** - Complete project overview
- **PROJECT_STATUS.md** - Current status and architecture
- **projectrequirment.md** - Hackathon requirements
- **mcp/business_mcp/README.md** - MCP server documentation
- **.claude/skills/*/SKILL.md** - Individual skill documentation

## 🧪 Testing

All components have been tested:

```bash
# Test MCP server
python mcp/business_mcp/test_server.py

# Test accounting (see scripts/accounting_manager_tests.md)
python scripts/accounting_manager.py validate

# Test CEO briefing (see scripts/ceo_briefing_tests.md)
python scripts/ceo_briefing.py generate
```

## 📈 Statistics

- **Total Files**: 80+ files
- **Lines of Code**: 5,000+ lines
- **Agent Skills**: 9 production-ready skills
- **MCP Servers**: 1 server with 3 actions
- **Git Commits**: 5 major commits
- **Documentation**: 15+ markdown files

## 🎓 Hackathon Information

**Event**: Panaversity Hackathon 0
**Theme**: Building Autonomous FTEs (Full-Time Equivalent)
**Tagline**: Your life and business on autopilot
**Approach**: Local-first, agent-driven, human-in-the-loop

### Weekly Research Meetings
Every Wednesday at 10:00 PM on Zoom
Join: https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1

## 🤝 Contributing

This is a hackathon project. For questions or collaboration:
- Review the documentation in this repository
- Join the Wednesday Research Meetings
- Check the Panaversity community resources

## 📝 License

Built for educational purposes as part of Panaversity Hackathon 0.

## 🙏 Acknowledgments

- **Panaversity** - For organizing the hackathon
- **Anthropic** - For Claude Code and Claude API
- **Community** - For support and collaboration

---

**Built with**: Python, Claude Code, Obsidian, Playwright, MCP
**Status**: Silver Tier Complete ✅ | Gold Tier In Progress 🚧
**Last Updated**: 2026-02-23

---

## Quick Commands Reference

```bash
# Financial Tracking
python scripts/accounting_manager.py log --type income --amount 250 --description "Payment"
python scripts/accounting_manager.py totals

# CEO Briefing
python scripts/ceo_briefing.py generate
python scripts/ceo_briefing.py view

# Task Management
python scripts/create_task_plan.py
python scripts/move_task.py Inbox Done task.md

# System Operations
python scripts/watcher_comprehensive.py  # File watcher
python scripts/scheduler.py              # Scheduler
python run_silver_tier.py                # Demo
```

For detailed usage, see **FINAL_SUMMARY.md** and individual skill documentation.
