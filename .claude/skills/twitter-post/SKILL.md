# Twitter Post Skill

Post tweets to Twitter and maintain a complete history.

## Trigger Phrases

- "Post to Twitter"
- "Tweet this"
- "Send a tweet"
- "Post on Twitter"
- "Share on Twitter"

## What This Skill Does

This skill allows you to post tweets to Twitter using the Twitter API v2. It:

1. Posts your tweet to Twitter
2. Logs the tweet to `AI_Employee_Vault/Reports/Twitter_History.md`
3. Integrates with the social summary system
4. Logs all activity to business.log
5. Handles errors gracefully

## Usage

### Post a Tweet

```bash
python scripts/post_twitter.py "Your tweet content here"
```

### Example

```bash
python scripts/post_twitter.py "Excited to share our new AI Employee system! #AI #Automation"
```

## Response Format

### Success

```json
{
  "success": true,
  "tweet_id": "1234567890",
  "content": "Your tweet content",
  "url": "https://twitter.com/user/status/1234567890"
}
```

### Error

```json
{
  "error": "Error message description"
}
```

## Configuration

### Environment Variables

Set these environment variables for Twitter API access:

```bash
export TWITTER_BEARER_TOKEN="your-bearer-token"
export TWITTER_API_KEY="your-api-key"
export TWITTER_API_SECRET="your-api-secret"
export TWITTER_ACCESS_TOKEN="your-access-token"
export TWITTER_ACCESS_SECRET="your-access-secret"
```

### Getting Twitter API Credentials

1. Go to https://developer.twitter.com/
2. Create a new app or use existing app
3. Generate API keys and tokens
4. Set the environment variables

## Features

### Automatic History Logging

All tweets are logged to `AI_Employee_Vault/Reports/Twitter_History.md`:

```markdown
# Twitter Post History

## February 2026

### 2026-02-24 at 14:30:00

**Tweet ID:** 1234567890
**Content:** Your tweet content here
**URL:** https://twitter.com/user/status/1234567890

---
```

### Social Summary Integration

Tweets are automatically logged to the social summary system for analytics and reporting.

### Business Log Integration

All Twitter activity is logged to `AI_Employee_Vault/Logs/business.log`:

```
[2026-02-24 14:30:00] TWITTER: Posted tweet: Your tweet content...
```

### Error Handling

- Character limit validation (280 characters)
- Empty content validation
- API authentication errors
- Network timeout handling
- Rate limit handling
- Complete error logging

## Limitations

- Maximum 280 characters per tweet
- Requires Twitter API v2 access
- Subject to Twitter API rate limits
- Requires valid API credentials

## Integration

### Scheduler Integration

Add to `scripts/scheduler.py` for automated tweeting:

```python
scheduler.add_task(
    name="daily_tweet",
    interval_seconds=86400,  # Daily
    command="scripts/post_twitter.py",
    args=["Daily update from AI Employee! #Automation"]
)
```

### CEO Briefing Integration

Twitter activity is included in weekly CEO briefings through the social summary system.

## Security

- Credentials stored in environment variables
- No hardcoded API keys
- Complete audit trail
- Error logging for security events

## Troubleshooting

### Authentication Failed

- Check all 5 environment variables are set
- Verify credentials are correct
- Check API app permissions

### Tweet Too Long

- Maximum 280 characters
- Shorten your message
- Consider thread support (future feature)

### Rate Limit Exceeded

- Twitter has rate limits
- Wait before posting again
- Check Twitter API documentation

### Network Errors

- Check internet connection
- Verify Twitter API is accessible
- Check firewall settings

## Files

- **Script:** `scripts/post_twitter.py`
- **History:** `AI_Employee_Vault/Reports/Twitter_History.md`
- **Business Log:** `AI_Employee_Vault/Logs/business.log`
- **Error Log:** `AI_Employee_Vault/Logs/error.log`

## API Reference

### post_tweet(content)

Posts a tweet to Twitter.

**Parameters:**
- `content` (string): Tweet content (max 280 characters)

**Returns:**
- Success: `{"success": true, "tweet_id": "...", "content": "...", "url": "..."}`
- Error: `{"error": "error message"}`

## Examples

### Simple Tweet

```bash
python scripts/post_twitter.py "Hello Twitter!"
```

### Tweet with Hashtags

```bash
python scripts/post_twitter.py "Check out our new feature! #AI #Automation #Tech"
```

### Tweet with Mention

```bash
python scripts/post_twitter.py "Thanks @username for the great feedback!"
```

## Future Enhancements

- Thread support (multiple tweets)
- Image/media attachments
- Poll creation
- Scheduled tweets
- Reply to tweets
- Retweet functionality
- Like/favorite tweets
- Analytics and engagement tracking

## Status

✅ **Production Ready**
- Twitter API v2 integration
- Complete history logging
- Error handling
- Social summary integration
- Business log integration

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Operational ✅
