# Social Summary System - Quick Reference

## 🚀 Quick Start

### View Your Social Activity
```bash
python scripts/social_summary.py view
```

### Log a Post Manually
```bash
# LinkedIn
python scripts/social_summary.py log --platform linkedin --content "Your post content" --date "2026-02-23"

# Facebook
python scripts/social_summary.py log --platform facebook --content "Your post content" --date "2026-02-23"

# Instagram
python scripts/social_summary.py log --platform instagram --content "Your post content" --date "2026-02-23"

# Twitter
python scripts/social_summary.py log --platform twitter --content "Your post content" --date "2026-02-23"
```

### Generate Summaries
```bash
# Daily summary
python scripts/social_summary.py summary --period day

# Weekly summary
python scripts/social_summary.py summary --period week

# Monthly summary
python scripts/social_summary.py summary --period month
```

---

## 📊 What Gets Tracked

- ✅ Platform (LinkedIn, Facebook, Instagram, Twitter)
- ✅ Post content (first 100 characters)
- ✅ Date and time
- ✅ Engagement metrics (when available)
- ✅ Post URL (when available)

---

## 🤖 Automatic Logging

### LinkedIn Posts
When you post to LinkedIn using the linkedin-post skill, the post is **automatically logged** to Social_Log.md. No manual action needed!

```bash
# This automatically logs to Social_Log.md
python scripts/post_linkedin.py "Your LinkedIn post content"
```

---

## 📁 Where to Find Your Data

### Social Activity Log
```
AI_Employee_Vault/Reports/Social_Log.md
```

### Business Log (includes social activity)
```
AI_Employee_Vault/Logs/business.log
```

---

## 📈 Sample Output

### Weekly Summary
```json
{
  "success": true,
  "period": "Week of Feb 23-01, 2026",
  "total_posts": 5,
  "by_platform": {
    "linkedin": 3,
    "facebook": 1,
    "instagram": 1,
    "twitter": 0
  },
  "total_engagement": 187,
  "average_engagement": 37.4
}
```

### Social_Log.md Format
```markdown
# Social Media Activity Log

Last updated: 2026-02-23 17:48:00

---

## February 2026

### Week 4 (Feb 23-01)

#### 2026-02-23

**LinkedIn Post**
- Time: 14:30:00
- Content: Excited to announce our new AI Employee system...
- Engagement: 45 likes, 12 comments
- URL: https://linkedin.com/posts/...

---

## Summary Statistics

### This Week
- Total Posts: 5
- LinkedIn: 3
- Facebook: 1
- Instagram: 1
- Twitter: 0
- Total Engagement: 187 interactions
```

---

## 🔧 Configuration

### Environment Variables (Optional)

```bash
# Enable automatic logging (default: true)
export SOCIAL_SUMMARY_AUTO_LOG=true

# Track engagement metrics (default: true)
export SOCIAL_SUMMARY_TRACK_ENGAGEMENT=true

# Log file location (default: AI_Employee_Vault/Reports/Social_Log.md)
export SOCIAL_SUMMARY_LOG_FILE="AI_Employee_Vault/Reports/Social_Log.md"

# CEO briefing integration (default: true)
export SOCIAL_SUMMARY_CEO_INTEGRATION=true
```

---

## 💡 Tips

1. **Automatic Logging**: LinkedIn posts are automatically logged - no manual work needed!

2. **Manual Logging**: Use manual logging for posts made outside the system (Facebook, Instagram, Twitter)

3. **Weekly Reviews**: Check your weekly summary every Sunday to track your social media activity

4. **CEO Briefing**: Social activity is automatically included in your weekly CEO briefing

5. **Audit Trail**: All social activity is logged to business.log for complete audit trail

---

## 🧪 Test the System

Run the integration test to verify everything works:

```bash
python scripts/social_integration_test.py
```

Expected output: `5/5 tests passed (100% success rate)`

---

## 📞 Common Commands

```bash
# View all social activity
python scripts/social_summary.py view

# Log a LinkedIn post
python scripts/social_summary.py log --platform linkedin --content "Post content" --date "2026-02-23"

# Get this week's summary
python scripts/social_summary.py summary --period week

# Get this month's summary
python scripts/social_summary.py summary --period month

# Test the system
python scripts/social_integration_test.py
```

---

## 🎯 Use Cases

### 1. Track Your Social Presence
Keep a complete record of all your social media posts in one place.

### 2. Analyze Posting Frequency
See how often you post on each platform with weekly/monthly summaries.

### 3. Monitor Engagement
Track likes, comments, and shares (when available).

### 4. Executive Reporting
Social activity automatically included in CEO briefing.

### 5. Audit Trail
Complete history of all social media activity for compliance.

---

## ⚡ Quick Examples

### Example 1: Post to LinkedIn (Automatic Logging)
```bash
python scripts/post_linkedin.py "Excited to share our latest product update!"
# ✓ Posted to LinkedIn
# ✓ Automatically logged to Social_Log.md
# ✓ Logged to business.log
```

### Example 2: Log a Facebook Post
```bash
python scripts/social_summary.py log \
  --platform facebook \
  --content "Check out our new blog post about AI automation!" \
  --date "2026-02-23"
```

### Example 3: View This Week's Activity
```bash
python scripts/social_summary.py summary --period week
```

---

## 🔍 Troubleshooting

### Posts Not Being Logged?
```bash
# Check if auto-logging is enabled
echo $SOCIAL_SUMMARY_AUTO_LOG

# View the log file
python scripts/social_summary.py view
```

### Can't Find Social_Log.md?
```bash
# It's located at:
AI_Employee_Vault/Reports/Social_Log.md
```

### Test Not Passing?
```bash
# Run the integration test
python scripts/social_integration_test.py

# Check for error messages
```

---

## 📚 More Information

For complete documentation, see:
- `SOCIAL_SUMMARY_COMPLETE.md` - Full system documentation
- `.claude/skills/social-summary/SKILL.md` - Agent skill documentation
- `scripts/social_summary_tests.md` - Test results

---

**Status:** ✅ Operational
**Test Coverage:** 100% (5/5 tests passed)
**Platforms Supported:** 4 (LinkedIn, Facebook, Instagram, Twitter)
**Integration:** CEO Briefing, Business Log, LinkedIn Post

---

# 🎉 Start Tracking Your Social Media Activity Today!
