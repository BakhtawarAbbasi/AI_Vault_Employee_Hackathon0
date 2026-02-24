# Personal AI Employee - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Personal AI Employee system from scratch.

---

## Prerequisites

### Required Software

- **Python 3.13+**
- **Claude Code CLI**
- **Obsidian** (for vault GUI)
- **Git** (for version control)

### Required Accounts

- Gmail account (for email integration)
- LinkedIn account (for social media)
- Twitter Developer account (for Twitter API)
- Meta Developer account (for Facebook/Instagram)
- Odoo instance (for accounting)

---

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd personal-ai-employee-hackathon
```

---

## Step 2: Environment Variables

Create `.env` file in project root:

```bash
# Gmail Configuration
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

# LinkedIn Configuration
LINKEDIN_ACCESS_TOKEN=your-linkedin-token

# Twitter Configuration
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token

# Meta (Facebook/Instagram) Configuration
META_ACCESS_TOKEN=your-meta-token
META_PAGE_ID=your-facebook-page-id
META_INSTAGRAM_ACCOUNT_ID=your-instagram-account-id

# Odoo Configuration
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your-database-name
ODOO_USERNAME=your-username
ODOO_PASSWORD=your-password
```

### Getting API Credentials

#### Gmail App Password
1. Go to Google Account settings
2. Enable 2-factor authentication
3. Generate app password for "Mail"
4. Copy password to `.env`

#### LinkedIn Access Token
1. Create LinkedIn app at https://www.linkedin.com/developers/
2. Request access to Share on LinkedIn API
3. Generate access token
4. Copy to `.env`

#### Twitter API
1. Apply for Twitter Developer account
2. Create new app
3. Generate API keys and tokens
4. Copy all credentials to `.env`

#### Meta (Facebook/Instagram)
1. Create Meta Developer account
2. Create new app
3. Add Facebook and Instagram products
4. Generate long-lived access token
5. Get Page ID and Instagram Account ID
6. Copy to `.env`

#### Odoo
1. Set up Odoo Community Edition instance
2. Create database
3. Create user with accounting permissions
4. Copy credentials to `.env`

---

## Step 3: Directory Structure

Create vault directory structure:

```bash
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Done,Needs_Approval,Approved}
mkdir -p AI_Employee_Vault/Personal/{Inbox,Needs_Action,Done,Notes}
mkdir -p AI_Employee_Vault/Cross_Domain/{Active,Archive}
mkdir -p AI_Employee_Vault/{Reports,Logs,Accounting,Calendar,Errors}
```

---

## Step 4: Initialize Data Files

Create initial data files:

```bash
# Calendar events
echo '{"events": [], "last_updated": "'$(date -Iseconds)'"}' > AI_Employee_Vault/Calendar/events.json

# Social log
touch AI_Employee_Vault/Logs/Social_Log.md
echo "# Social Media Activity Log" > AI_Employee_Vault/Logs/Social_Log.md

# Business log
touch AI_Employee_Vault/Logs/business.log

# Error log
touch AI_Employee_Vault/Logs/error.log

# Social log
touch AI_Employee_Vault/Logs/social.log

# Routing log
touch AI_Employee_Vault/Logs/routing.log
```

---

## Step 5: Configure Obsidian

1. Open Obsidian
2. Open vault: `AI_Employee_Vault`
3. Install recommended plugins:
   - Dataview (for task queries)
   - Templater (for task templates)
   - Calendar (for date navigation)

---

## Step 6: Test MCP Servers

### Test Business MCP

```bash
# Test email sending (dry run)
python mcp/business_mcp/server.py send_email '{
  "to": "test@example.com",
  "subject": "Test Email",
  "body": "This is a test"
}'
```

### Test Odoo MCP

```bash
# Test invoice listing
python mcp/odoo_mcp/server.py list_invoices '{
  "limit": 5
}'
```

### Test Calendar MCP

```bash
# Test event creation
python mcp/calendar_mcp/server.py create_event '{
  "title": "Test Event",
  "start_time": "2026-02-25T10:00:00",
  "end_time": "2026-02-25T11:00:00"
}'
```

---

## Step 7: Test Agent Skills

### Test Twitter Posting

```bash
python scripts/post_twitter.py "Test tweet from Personal AI Employee"
```

### Test Meta Posting

```bash
# Facebook
python scripts/post_meta.py facebook "Test post from Personal AI Employee"

# Instagram
python scripts/post_meta.py instagram "Test post" --image-url "https://example.com/image.jpg"
```

### Test Personal Tasks

```bash
# Create personal task
python scripts/personal_tasks.py create-task "Test personal task" "This is a test"
```

---

## Step 8: Start Scheduler

Start the scheduler to enable automated task processing:

```bash
python scripts/scheduler.py
```

The scheduler will run 10 automated tasks:
1. LinkedIn monitor (every 10 minutes)
2. Process inbox (every 5 minutes)
3. CEO briefing (weekly)
4. Accounting summary (weekly)
5. Error recovery (every minute)
6. Ralph Wiggum loop (every 30 seconds)
7. Personal inbox (hourly)
8. Social summary (weekly)
9. Cross-domain processing (hourly)
10. Unified report (daily)

---

## Step 9: Verify Installation

### Check Logs

```bash
# Check business log
tail -20 AI_Employee_Vault/Logs/business.log

# Check for errors
tail -20 AI_Employee_Vault/Logs/error.log

# Check scheduler status
ps aux | grep scheduler.py
```

### Check Task Flow

1. Create test task in `AI_Employee_Vault/Inbox/TEST.md`
2. Wait 30 seconds for Ralph Wiggum loop
3. Check if task moved to appropriate folder
4. Review business.log for activity

---

## Step 10: Configure Claude Code

Add MCP servers to Claude Code configuration:

```json
{
  "mcpServers": {
    "business-mcp": {
      "command": "python",
      "args": ["mcp/business_mcp/server.py"]
    },
    "odoo-mcp": {
      "command": "python",
      "args": ["mcp/odoo_mcp/server.py"]
    },
    "calendar-mcp": {
      "command": "python",
      "args": ["mcp/calendar_mcp/server.py"]
    }
  }
}
```

---

## Troubleshooting

### Scheduler Not Running

**Problem:** Scheduler stops unexpectedly

**Solution:**
```bash
# Check for errors
tail -50 AI_Employee_Vault/Logs/error.log

# Restart scheduler
pkill -f scheduler.py
python scripts/scheduler.py
```

### API Authentication Errors

**Problem:** "Authentication failed" errors

**Solution:**
1. Verify credentials in `.env`
2. Check token expiration
3. Regenerate tokens if needed
4. Restart scheduler

### Tasks Not Processing

**Problem:** Tasks stuck in Inbox

**Solution:**
1. Check Ralph Wiggum loop is running
2. Verify task format (must have checkboxes)
3. Check error.log for issues
4. Manually trigger: `python scripts/ralph_wiggum.py process-all`

### MCP Server Errors

**Problem:** MCP server returns errors

**Solution:**
1. Test server directly: `python mcp/<server>/server.py <action> '{}'`
2. Check environment variables
3. Verify API connectivity
4. Review error.log

---

## Maintenance

### Daily

- Review business.log for activity
- Check error.log for issues
- Review /Needs_Approval/ for pending actions

### Weekly

- Review CEO briefing
- Check unified report
- Review social summary
- Archive old logs (optional)

### Monthly

- Rotate logs if needed
- Update API credentials if expired
- Backup vault to external storage
- Review and update agent skills

---

## Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use app passwords** - Never use main account passwords
3. **Rotate tokens regularly** - Update every 90 days
4. **Review approval files** - Always check before moving to /Approved/
5. **Monitor logs** - Check error.log daily
6. **Backup vault** - Use Git for version control
7. **Limit API permissions** - Only grant necessary scopes

---

## Performance Optimization

### For Large Vaults

- Enable log rotation (weekly)
- Archive old tasks (monthly)
- Use database for events (if >10,000 events)
- Increase scheduler intervals

### For Multiple Users

- Deploy to cloud VM
- Use separate vaults per user
- Implement queue system
- Add load balancing

---

## Cloud Deployment (Optional)

### Oracle Cloud Free Tier

1. Create Oracle Cloud account
2. Launch Ubuntu VM (Always Free tier)
3. Install Python 3.13+
4. Clone repository
5. Configure environment variables
6. Set up systemd service for scheduler
7. Configure firewall rules
8. Set up vault sync (Git or Syncthing)

### Systemd Service

Create `/etc/systemd/system/ai-employee.service`:

```ini
[Unit]
Description=Personal AI Employee Scheduler
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/personal-ai-employee-hackathon
ExecStart=/usr/bin/python3 scripts/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ai-employee
sudo systemctl start ai-employee
sudo systemctl status ai-employee
```

---

## Monitoring

### Health Checks

```bash
# Check scheduler status
systemctl status ai-employee

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

## Backup and Recovery

### Backup Strategy

```bash
# Backup vault (Git)
cd AI_Employee_Vault
git add .
git commit -m "Backup $(date +%Y-%m-%d)"
git push

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz AI_Employee_Vault/Logs/

# Backup configuration
cp .env .env.backup
```

### Recovery

```bash
# Restore vault from Git
git clone <vault-repo-url> AI_Employee_Vault

# Restore configuration
cp .env.backup .env

# Restart scheduler
python scripts/scheduler.py
```

---

## Upgrading

### Update Code

```bash
git pull origin main
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Migrate Data

Check `CHANGELOG.md` for migration instructions between versions.

---

## Support

- **Documentation:** See `README.md` and `ARCHITECTURE.md`
- **Issues:** Check `AI_Employee_Vault/Logs/error.log`
- **Community:** [GitHub Issues](https://github.com/your-repo/issues)

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Production Ready ✅
