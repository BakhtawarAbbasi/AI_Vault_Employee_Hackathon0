# Social Summary Agent Skill

## Overview

The Social Summary skill automatically logs all social media activity to a centralized Social_Log.md file, providing a complete audit trail of all posts, engagement, and social media interactions.

## Capabilities

1. **Social Media Logging**
   - Log all LinkedIn posts automatically
   - Track Facebook posts (when integrated)
   - Track Instagram posts (when integrated)
   - Track Twitter/X posts (when integrated)
   - Centralized log file

2. **Activity Tracking**
   - Platform identification
   - Post content
   - Timestamp
   - Engagement metrics (when available)
   - Post URL (when available)

3. **Summary Generation**
   - Daily social media summary
   - Weekly social media report
   - Monthly analytics
   - Platform comparison

4. **Integration**
   - Works with linkedin-post skill
   - Integrates with CEO briefing
   - Logs to business.log
   - Automatic after every post

## Usage

### Automatic Logging

The social summary system runs automatically after every social media post. No manual intervention required.

### Manual Operations

```bash
# View social log
python scripts/social_summary.py view

# Add manual entry
python scripts/social_summary.py log --platform linkedin --content "Post content" --date "2026-02-23"

# Generate daily summary
python scripts/social_summary.py summary --period day

# Generate weekly summary
python scripts/social_summary.py summary --period week

# Generate monthly summary
python scripts/social_summary.py summary --period month
```

### Trigger Phrases

When the user says any of these, invoke this skill:

- "Show social media activity"
- "What did I post today?"
- "Social media log"
- "Show LinkedIn posts"
- "Social media summary"
- "What's my social presence?"
- "Show posting history"

## Social_Log.md Format

```markdown
# Social Media Activity Log

Last updated: 2026-02-23 17:17:40

---

## February 2026

### Week 4 (Feb 17-23)

#### 2026-02-23

**LinkedIn Post**
- Time: 14:30:00
- Content: Excited to announce our new AI Employee system! It automates business tasks and increases efficiency. #AI #Automation
- Engagement: 45 likes, 12 comments, 8 shares
- URL: https://linkedin.com/posts/...

**LinkedIn Post**
- Time: 10:15:00
- Content: Just completed a major milestone in our project. Thanks to the amazing team! #TeamWork #Success
- Engagement: 32 likes, 5 comments
- URL: https://linkedin.com/posts/...

#### 2026-02-22

**LinkedIn Post**
- Time: 16:45:00
- Content: Industry insights on AI automation trends for 2026. Read more in our latest blog post.
- Engagement: 28 likes, 7 comments
- URL: https://linkedin.com/posts/...

---

## Summary Statistics

### This Week (Feb 17-23)
- Total Posts: 5
- LinkedIn: 5
- Facebook: 0
- Instagram: 0
- Twitter: 0
- Total Engagement: 187 interactions

### This Month (February 2026)
- Total Posts: 18
- LinkedIn: 15
- Facebook: 2
- Instagram: 1
- Twitter: 0
- Total Engagement: 842 interactions

---

*Maintained by Social Summary System*
```

## Workflow

### 1. Post Detection

When a social media post is created:

```python
# After LinkedIn post
post_data = {
    'platform': 'linkedin',
    'content': 'Post content here...',
    'timestamp': '2026-02-23T14:30:00Z',
    'engagement': {'likes': 0, 'comments': 0, 'shares': 0},
    'url': 'https://linkedin.com/posts/...'
}

social_summary.log_post(post_data)
```

### 2. Log Entry Creation

```python
def log_post(post_data):
    # Read existing log
    log_file = "AI_Employee_Vault/Reports/Social_Log.md"

    # Add new entry
    entry = f"""
#### {post_data['date']}

**{post_data['platform'].title()} Post**
- Time: {post_data['time']}
- Content: {post_data['content']}
- Engagement: {post_data['engagement']}
- URL: {post_data['url']}
"""

    # Update log file
    append_to_log(log_file, entry)

    # Update statistics
    update_statistics()
```

### 3. Statistics Update

After each post, update summary statistics:

```python
def update_statistics():
    # Count posts by platform
    # Calculate total engagement
    # Update weekly/monthly summaries
    # Save to log file
```

### 4. Integration with CEO Briefing

Social media activity is automatically included in weekly CEO briefing:

```python
# In ceo_briefing.py
social_activity = get_social_summary(week_start, week_end)

briefing += f"""
### Social Media Activity ({social_activity['total_posts']} posts)
- LinkedIn: {social_activity['linkedin_posts']} posts
- Total Engagement: {social_activity['total_engagement']} interactions
"""
```

## Integration Points

### With Other Skills

- **linkedin-post**: Automatically log after posting
- **ceo-briefing**: Include social activity in weekly report
- **business-mcp**: Log activity to business.log
- **ralph-wiggum**: Track social tasks completion

### With MCP Server

- **log_activity**: Log all social posts to business.log
- **post_linkedin**: Automatically trigger social summary

## Examples

### Example 1: View Social Log

```bash
python scripts/social_summary.py view
```

**Output:**
```
# Social Media Activity Log

Last updated: 2026-02-23 17:17:40

## February 2026

### Week 4 (Feb 17-23)

#### 2026-02-23
- LinkedIn Post (14:30): "Excited to announce our new AI Employee system..."
- LinkedIn Post (10:15): "Just completed a major milestone..."

Total posts this week: 5
Total engagement: 187 interactions
```

### Example 2: Add Manual Entry

```bash
python scripts/social_summary.py log \
  --platform linkedin \
  --content "New blog post about AI automation" \
  --date "2026-02-23"
```

**Output:**
```json
{
  "success": true,
  "message": "Social media post logged successfully",
  "platform": "linkedin",
  "date": "2026-02-23"
}
```

### Example 3: Generate Weekly Summary

```bash
python scripts/social_summary.py summary --period week
```

**Output:**
```json
{
  "success": true,
  "period": "Week of Feb 17-23, 2026",
  "total_posts": 5,
  "by_platform": {
    "linkedin": 5,
    "facebook": 0,
    "instagram": 0,
    "twitter": 0
  },
  "total_engagement": 187,
  "average_engagement": 37.4,
  "most_engaged_post": {
    "platform": "linkedin",
    "content": "Excited to announce our new AI Employee system...",
    "engagement": 65
  }
}
```

### Example 4: Generate Monthly Summary

```bash
python scripts/social_summary.py summary --period month
```

**Output:**
```json
{
  "success": true,
  "period": "February 2026",
  "total_posts": 18,
  "by_platform": {
    "linkedin": 15,
    "facebook": 2,
    "instagram": 1,
    "twitter": 0
  },
  "total_engagement": 842,
  "average_engagement": 46.8,
  "posting_frequency": "3.6 posts per week",
  "best_day": "Wednesday",
  "best_time": "14:00-16:00"
}
```

## Configuration

Set these environment variables:

```bash
# Enable automatic logging (default: true)
export SOCIAL_SUMMARY_AUTO_LOG=true

# Include engagement metrics (default: true)
export SOCIAL_SUMMARY_TRACK_ENGAGEMENT=true

# Log file location (default: AI_Employee_Vault/Reports/Social_Log.md)
export SOCIAL_SUMMARY_LOG_FILE="AI_Employee_Vault/Reports/Social_Log.md"

# Update CEO briefing (default: true)
export SOCIAL_SUMMARY_CEO_INTEGRATION=true
```

## Log Entry Structure

Each log entry includes:

```markdown
#### YYYY-MM-DD

**Platform Post**
- Time: HH:MM:SS
- Content: [First 100 characters of post content]
- Engagement: X likes, Y comments, Z shares
- URL: [Post URL if available]
- Status: Published/Scheduled/Draft
```

## Statistics Tracking

### Daily Statistics
- Total posts
- Posts by platform
- Total engagement
- Average engagement per post

### Weekly Statistics
- Total posts
- Posts by platform
- Total engagement
- Average engagement per post
- Best performing post
- Posting frequency

### Monthly Statistics
- Total posts
- Posts by platform
- Total engagement
- Average engagement per post
- Best performing post
- Posting frequency
- Best day for posting
- Best time for posting
- Engagement trends

## Integration with LinkedIn Post Skill

Modify `scripts/post_linkedin.py` to automatically log:

```python
# After successful LinkedIn post
result = post_to_linkedin(content)

if result['success']:
    # Log to social summary
    subprocess.run([
        'python', 'scripts/social_summary.py', 'log',
        '--platform', 'linkedin',
        '--content', content,
        '--date', datetime.now().strftime('%Y-%m-%d')
    ])
```

## Best Practices

1. **Log Immediately** - Log posts right after publishing
2. **Track Engagement** - Update engagement metrics regularly
3. **Review Weekly** - Check social summary in CEO briefing
4. **Analyze Trends** - Use monthly summaries to optimize posting
5. **Archive Regularly** - Archive old logs to keep file manageable

## Troubleshooting

### Issue: Posts not being logged

**Solution:** Check if auto-logging is enabled
```bash
echo $SOCIAL_SUMMARY_AUTO_LOG
python scripts/social_summary.py view
```

### Issue: Engagement metrics missing

**Solution:** Enable engagement tracking
```bash
export SOCIAL_SUMMARY_TRACK_ENGAGEMENT=true
```

### Issue: Log file too large

**Solution:** Archive old entries
```bash
python scripts/social_summary.py archive --before 2026-01-01
```

## Future Enhancements

- Engagement tracking via API
- Sentiment analysis of comments
- Optimal posting time recommendations
- Content performance analytics
- Hashtag effectiveness tracking
- Competitor analysis
- Multi-platform cross-posting

---

**Skill Type:** Agent Skill (Automated)
**Dependencies:** Python 3.13+, scripts/social_summary.py
**Schedule:** After every social media post
**Security Level:** Low (read-only logging)
**Approval Required:** No (automatic logging)
