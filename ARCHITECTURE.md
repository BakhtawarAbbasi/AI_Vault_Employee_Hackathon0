# Personal AI Employee - System Architecture

## Architecture Overview

This document provides a comprehensive overview of the Personal AI Employee system architecture, component interactions, and deployment guidelines.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PERSONAL AI EMPLOYEE SYSTEM                          │
│                           Architecture v1.0                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SOURCES                                  │
├─────────────┬─────────────┬─────────────┬─────────────┬────────────────────┤
│   Gmail     │  WhatsApp   │  LinkedIn   │  Bank APIs  │  Social Media      │
│             │             │             │             │  (Twitter/FB/IG)   │
└──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┴──────┬─────────────┘
       │             │             │             │             │
       ▼             ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PERCEPTION LAYER                                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │
│  │Gmail Watcher │ │WhatsApp Watch│ │LinkedIn Watch│ │Finance Watch │      │
│  │  (Python)    │ │ (Playwright) │ │  (Python)    │ │  (Python)    │      │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘      │
└─────────┼────────────────┼────────────────┼────────────────┼───────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Local Storage)                           │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  BUSINESS DOMAIN              │  PERSONAL DOMAIN                      │ │
│  ├───────────────────────────────┼───────────────────────────────────────┤ │
│  │  /Inbox/                      │  /Personal/Inbox/                     │ │
│  │  /Needs_Action/               │  /Personal/Needs_Action/              │ │
│  │  /Done/                       │  /Personal/Done/                      │ │
│  │  /Needs_Approval/             │  /Personal/Notes/                     │ │
│  ├───────────────────────────────┴───────────────────────────────────────┤ │
│  │  CROSS-DOMAIN                                                         │ │
│  │  /Cross_Domain/  (Tasks spanning both domains)                        │ │
│  ├───────────────────────────────────────────────────────────────────────┤ │
│  │  SHARED RESOURCES                                                     │ │
│  │  /Reports/  /Logs/  /Accounting/  /Calendar/  /Errors/               │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REASONING LAYER                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         CLAUDE CODE                                   │ │
│  │  Read → Analyze → Plan → Execute → Validate → Complete               │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │  RALPH WIGGUM LOOP (Autonomous Execution)                       │ │ │
│  │  │  • Max 5 iterations per task                                    │ │ │
│  │  │  • Automatic completion detection                               │ │ │
│  │  │  • Safety mechanisms for risky operations                       │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
              ┌──────────────────┴───────────────────┐
              ▼                                      ▼
┌──────────────────────────────┐    ┌────────────────────────────────────────┐
│   HUMAN-IN-THE-LOOP          │    │         ACTION LAYER                   │
│  ┌────────────────────────┐  │    │  ┌──────────────────────────────────┐ │
│  │ Review Approval Files  │──┼───▶│  │    MCP SERVERS (3 Total)         │ │
│  │ Move to /Approved      │  │    │  │  ┌────────────┬────────────────┐ │ │
│  └────────────────────────┘  │    │  │  │ Business   │ Odoo           │ │ │
│                              │    │  │  │ MCP        │ MCP            │ │ │
└──────────────────────────────┘    │  │  │ • Email    │ • Invoices     │ │ │
                                    │  │  │ • LinkedIn │ • Payments     │ │ │
                                    │  │  │ • Logging  │ • Accounting   │ │ │
                                    │  │  └────────────┴────────────────┘ │ │
                                    │  │  ┌────────────────────────────┐  │ │
                                    │  │  │ Calendar MCP               │  │ │
                                    │  │  │ • Create Events            │  │ │
                                    │  │  │ • List Events              │  │ │
                                    │  │  │ • Update/Delete Events     │  │ │
                                    │  │  └────────────────────────────┘  │ │
                                    │  └──────────────────────────────────┘ │
                                    └────────────────────────────────────────┘
                                                     │
                                                     ▼
                                    ┌────────────────────────────────────────┐
                                    │      EXTERNAL ACTIONS                  │
                                    │  • Send Emails                         │
                                    │  • Post to Social Media (5 platforms)  │
                                    │  • Create Invoices                     │
                                    │  • Record Payments                     │
                                    │  • Schedule Events                     │
                                    └────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │              SCHEDULER (10 Automated Tasks)                           │ │
│  │  • LinkedIn Monitor (10 min)    • Process Inbox (5 min)              │ │
│  │  • CEO Briefing (weekly)        • Accounting Summary (weekly)        │ │
│  │  • Error Recovery (1 min)       • Ralph Wiggum Loop (30 sec)         │ │
│  │  • Personal Inbox (1 hour)      • Social Summary (weekly)            │ │
│  │  • Cross-Domain (1 hour)        • Unified Report (daily)             │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │              CROSS-DOMAIN ROUTER                                      │ │
│  │  • Task Classification          • Domain Routing                      │ │
│  │  • Linked Task Creation         • Unified Reporting                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT SKILLS LAYER (15 Total)                       │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┬──────────────┐ │
│  │ gmail-send  │linkedin-post│twitter-post │ social-meta │ personal-    │ │
│  │             │             │             │ (FB/IG)     │ tasks        │ │
│  ├─────────────┼─────────────┼─────────────┼─────────────┼──────────────┤ │
│  │ vault-file  │human-       │task-planner │linkedin-    │ file-triage  │ │
│  │ manager     │approval     │             │watcher      │              │ │
│  ├─────────────┼─────────────┼─────────────┼─────────────┼──────────────┤ │
│  │ accounting  │ceo-briefing │error-       │ralph-wiggum │ social-      │ │
│  │ manager     │             │recovery     │             │ summary      │ │
│  ├─────────────┴─────────────┴─────────────┴─────────────┴──────────────┤ │
│  │ cross-domain (NEW)                                                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         LOGGING & MONITORING                                │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  business.log  │  error.log  │  social.log  │  routing.log           │ │
│  │  Complete audit trail for all system operations                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Descriptions

### 1. Perception Layer (Watchers)

**Purpose:** Monitor external sources and create actionable tasks

**Components:**
- **Gmail Watcher:** Monitors inbox for important emails
- **WhatsApp Watcher:** Monitors WhatsApp for urgent messages
- **LinkedIn Watcher:** Monitors LinkedIn for engagement opportunities
- **Finance Watcher:** Monitors bank transactions and financial data

**Technology:** Python scripts with API integrations

### 2. Storage Layer (Obsidian Vault)

**Purpose:** Local-first data storage and knowledge base

**Structure:**
- **Business Domain:** Work-related tasks and projects
- **Personal Domain:** Personal tasks and notes
- **Cross-Domain:** Tasks spanning both domains
- **Shared Resources:** Reports, logs, accounting, calendar

**Technology:** Markdown files in structured directories

### 3. Reasoning Layer (Claude Code)

**Purpose:** AI-powered task analysis and execution

**Features:**
- Read and analyze tasks
- Create execution plans
- Execute multi-step workflows
- Validate results
- Complete tasks autonomously

**Technology:** Claude Code with Ralph Wiggum loop

### 4. Action Layer (MCP Servers)

**Purpose:** Execute external actions

**Servers:**
1. **Business MCP:** Email, LinkedIn, logging
2. **Odoo MCP:** Invoices, payments, accounting
3. **Calendar MCP:** Event management

**Technology:** Python-based MCP servers

### 5. Orchestration Layer

**Purpose:** Coordinate system operations

**Components:**
- **Scheduler:** 10 automated tasks running 24/7
- **Cross-Domain Router:** Route tasks between domains

**Technology:** Python scheduler with task management

### 6. Agent Skills Layer

**Purpose:** Modular AI capabilities

**Count:** 16 agent skills covering all functionality

**Technology:** Claude Code agent skills

### 7. Logging & Monitoring

**Purpose:** Complete audit trail

**Logs:**
- business.log: All operations
- error.log: Errors and failures
- social.log: Social media activity
- routing.log: Cross-domain routing

---

## Data Flow Examples

### Example 1: Email to Task Flow

```
1. Gmail Watcher detects important email
2. Creates task in /Inbox/EMAIL_xxx.md
3. Scheduler triggers Ralph Wiggum loop
4. Claude Code reads email task
5. Analyzes content and creates plan
6. Executes response (via Business MCP)
7. Logs activity to business.log
8. Moves task to /Done/
```

### Example 2: Cross-Domain Task Flow

```
1. Task created: "Schedule client meeting and arrange childcare"
2. Cross-Domain Router classifies as cross-domain
3. Creates linked task in Business/Needs_Action
4. Creates linked task in Personal/Needs_Action
5. Both tasks reference each other
6. Original task archived in Cross_Domain/Archive
7. Each domain processes its task independently
8. Unified report shows both tasks
```

### Example 3: Social Media Post Flow

```
1. User/System creates post content
2. Agent skill invoked (twitter-post, social-meta, etc.)
3. MCP server posts to platform
4. Post logged to social.log
5. Post logged to Social_Log.md
6. Social summary system updated
7. Statistics calculated
8. Included in next CEO briefing
```

---

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| AI Engine | Claude Code | Reasoning and execution |
| Storage | Obsidian (Markdown) | Local-first knowledge base |
| Orchestration | Python 3.13+ | Scheduling and coordination |
| MCP Servers | Python | External action execution |
| Watchers | Python + APIs | External monitoring |

### Key Libraries

- **pathlib:** File system operations
- **json:** Data serialization
- **datetime:** Time management
- **logging:** System logging
- **subprocess:** Process management
- **requests:** HTTP requests (social media APIs)
- **playwright:** Browser automation (WhatsApp)

### External Integrations

- **Gmail API:** Email monitoring and sending
- **LinkedIn API:** Social media posting
- **Twitter API v2:** Tweet posting
- **Meta Graph API:** Facebook/Instagram posting
- **Odoo JSON-RPC:** Accounting integration

---

## Security Architecture

### Credential Management

- All credentials stored in environment variables
- No hardcoded secrets in code
- .env file for local development (gitignored)
- Separate credentials for each service

### Human-in-the-Loop (HITL)

- Sensitive actions require approval
- Approval files in /Needs_Approval/
- User moves to /Approved/ to proceed
- Complete audit trail

### Data Privacy

- All data stored locally
- No cloud storage of sensitive data
- Local-first architecture
- Complete control over data

### Audit Trail

- Every action logged
- Timestamp, actor, target, result
- 4 separate log files for different purposes
- Logs retained indefinitely

---

## Scalability Considerations

### Current Capacity

- **Tasks:** Unlimited (file-based storage)
- **Events:** Unlimited (JSON storage)
- **Logs:** Grows over time (consider rotation)
- **Social Posts:** Unlimited (markdown storage)

### Performance

- **Task Processing:** ~30 seconds per task
- **Scheduler Overhead:** Minimal (<1% CPU)
- **Storage Growth:** ~1MB per 1000 tasks
- **API Rate Limits:** Varies by service

### Future Scaling

- Database migration for large datasets
- Log rotation for long-term operation
- Distributed processing for multiple agents
- Cloud deployment for 24/7 operation

---

## Deployment Architecture

### Local Deployment (Current)

```
User's Machine
├── Claude Code (AI Engine)
├── Obsidian (GUI/Storage)
├── Python Scripts (Watchers, MCP, Scheduler)
└── Environment Variables (Credentials)
```

**Pros:**
- Complete privacy
- No cloud costs
- Full control
- Low latency

**Cons:**
- Requires machine to be on
- No remote access
- Single point of failure

### Cloud Deployment (Future - Platinum Tier)

```
Cloud VM (Oracle/AWS)
├── Watchers (24/7 monitoring)
├── Scheduler (24/7 automation)
├── MCP Servers (always available)
└── Vault Sync (Git/Syncthing)

Local Machine
├── Claude Code (approvals)
├── Obsidian (GUI)
└── Sensitive Actions (payments, WhatsApp)
```

**Pros:**
- 24/7 operation
- Remote access
- High availability
- Automatic failover

**Cons:**
- Cloud costs
- More complex setup
- Security considerations

---

## Monitoring & Health Checks

### System Health Indicators

1. **Scheduler Status:** All 10 tasks running
2. **Log Growth:** Logs being written regularly
3. **Task Flow:** Tasks moving through workflow
4. **Error Rate:** Low error count in error.log
5. **API Status:** External APIs responding

### Monitoring Commands

```bash
# Check scheduler status
ps aux | grep scheduler.py

# Check recent activity
tail -20 AI_Employee_Vault/Logs/business.log

# Check for errors
tail -20 AI_Employee_Vault/Logs/error.log

# Check task counts
python scripts/cross_domain_router.py unified-report
```

### Alerting (Future)

- Email alerts for critical errors
- Slack notifications for important events
- Dashboard for system health
- Automated recovery procedures

---

## Maintenance Procedures

### Daily Maintenance

- Review business.log for activity
- Check error.log for issues
- Review /Needs_Approval/ for pending actions

### Weekly Maintenance

- Review CEO briefing
- Check unified report for work-life balance
- Review social summary
- Archive old logs (optional)

### Monthly Maintenance

- Rotate logs if needed
- Review and update agent skills
- Update API credentials if expired
- Backup vault to external storage

### Quarterly Maintenance

- Full system audit
- Security review
- Performance optimization
- Feature updates

---

## Disaster Recovery

### Backup Strategy

1. **Vault Backup:** Git repository (automatic)
2. **Logs Backup:** Copy to external storage (weekly)
3. **Credentials Backup:** Secure password manager
4. **Configuration Backup:** .env file (encrypted)

### Recovery Procedures

1. **Lost Vault:** Restore from Git
2. **Corrupted Logs:** Regenerate from vault
3. **Lost Credentials:** Restore from password manager
4. **System Crash:** Restart scheduler and watchers

### Data Retention

- **Vault:** Indefinite (Git history)
- **Logs:** 90 days minimum
- **Backups:** 30 days rolling
- **Archives:** Indefinite

---

## Performance Metrics

### Current Performance

- **Task Processing Time:** 10-60 seconds per task
- **Scheduler Cycle Time:** 1 second
- **API Response Time:** 1-5 seconds
- **Storage Growth:** ~100KB per day

### Optimization Opportunities

- Parallel task processing
- Caching for repeated operations
- Database for large datasets
- Async operations for I/O

---

## Future Architecture Enhancements

### Phase 1: Enhanced Automation

- Automatic task prioritization
- Smart scheduling based on urgency
- Predictive task creation
- Intelligent routing

### Phase 2: Multi-Agent System

- Specialized agents for different domains
- Agent-to-agent communication
- Distributed task processing
- Collaborative problem solving

### Phase 3: Cloud Integration

- Hybrid cloud/local deployment
- 24/7 cloud watchers
- Local approval and sensitive actions
- Vault synchronization

### Phase 4: Advanced Features

- Natural language task creation
- Voice interface
- Mobile app
- Real-time collaboration

---

**Document Version:** 1.0
**Last Updated:** 2026-02-24
**Status:** Complete ✅
