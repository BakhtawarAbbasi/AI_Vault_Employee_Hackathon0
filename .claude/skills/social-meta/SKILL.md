# Social Meta Skill (Facebook + Instagram)

Post to Facebook and Instagram using Meta Graph API.

## Trigger Phrases

- "Post to Facebook"
- "Share on Facebook"
- "Post to Instagram"
- "Share on Instagram"
- "Post to Meta platforms"

## What This Skill Does

This skill allows you to post to Facebook and Instagram using the Meta Graph API. It:

1. Posts content to Facebook pages
2. Posts images with captions to Instagram
3. Logs all posts to `AI_Employee_Vault/Logs/social.log`
4. Integrates with the social summary system
5. Logs all activity to business.log
6. Handles errors gracefully

## Usage

### Post to Facebook

```bash
python scripts/post_meta.py facebook "Your post content here"

# With link
python scripts/post_meta.py facebook "Check out this article!" "https://example.com"
```

### Post to Instagram

```bash
# Instagram requires an image URL
python scripts/post_meta.py instagram "Your caption here" "https://example.com/image.jpg"
```

## Response Format

### Success

```json
{
  "success": true,
  "platform": "facebook",
  "post_id": "123456789_987654321",
  "content": "Your post content",
  "url": "https://facebook.com/123456789_987654321"
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

Set these environment variables for Meta API access:

#### Facebook

```bash
export FACEBOOK_ACCESS_TOKEN="your-page-access-token"
export FACEBOOK_PAGE_ID="your-page-id"
```

#### Instagram

```bash
export INSTAGRAM_ACCESS_TOKEN="your-instagram-access-token"
export INSTAGRAM_ACCOUNT_ID="your-instagram-business-account-id"
```

### Getting Meta API Credentials

#### Facebook

1. Go to https://developers.facebook.com/
2. Create an app or use existing app
3. Add "Pages" product
4. Generate a Page Access Token
5. Get your Page ID from your Facebook page settings

#### Instagram

1. Convert your Instagram account to a Business account
2. Link it to a Facebook page
3. Use the same app from Facebook setup
4. Add "Instagram" product
5. Get Instagram Business Account ID from Graph API Explorer

## Features

### Facebook Features

- Post text updates
- Share links with preview
- Automatic link unfurling
- Page posting (not personal profile)

### Instagram Features

- Post images with captions
- Requires publicly accessible image URL
- Business account required
- Two-step process (create container, then publish)

### Logging

All posts are logged to multiple locations:

#### social.log

`AI_Employee_Vault/Logs/social.log`:

```
[2026-02-24 14:30:00] FACEBOOK: Posted - ID: 123_456 - Content: Your post content...
[2026-02-24 14:35:00] INSTAGRAM: Posted - ID: 789 - Content: Your caption...
```

#### business.log

`AI_Employee_Vault/Logs/business.log`:

```
[2026-02-24 14:30:00] META_SOCIAL: Posted to Facebook: Your post content...
[2026-02-24 14:35:00] META_SOCIAL: Posted to Instagram: Your caption...
```

#### Social Summary Integration

All posts are automatically logged to the social summary system for analytics and CEO briefing integration.

### Error Handling

- Empty content validation
- Missing credentials detection
- API authentication errors
- Network timeout handling
- Rate limit handling
- Complete error logging

## Limitations

### Facebook

- Requires Page Access Token (not User Access Token)
- Can only post to pages you manage
- Subject to Facebook API rate limits
- Link previews may take time to generate

### Instagram

- Requires Business or Creator account
- Must provide publicly accessible image URL
- Cannot post videos (future feature)
- Cannot post to personal accounts
- Subject to Instagram API rate limits
- Image must be accessible via HTTPS

## Integration

### Scheduler Integration

Add to `scripts/scheduler.py` for automated posting:

```python
# Daily Facebook update
scheduler.add_task(
    name="daily_facebook_post",
    interval_seconds=86400,  # Daily
    command="scripts/post_meta.py",
    args=["facebook", "Daily update from AI Employee!"]
)

# Weekly Instagram post
scheduler.add_task(
    name="weekly_instagram_post",
    interval_seconds=604800,  # Weekly
    command="scripts/post_meta.py",
    args=["instagram", "Weekly highlights! #AI", "https://example.com/image.jpg"]
)
```

### CEO Briefing Integration

Facebook and Instagram activity is included in weekly CEO briefings through the social summary system.

## Security

- Credentials stored in environment variables
- No hardcoded API keys
- Complete audit trail
- Error logging for security events
- Separate logs for social activity

## Troubleshooting

### Facebook Issues

#### Authentication Failed

- Check `FACEBOOK_ACCESS_TOKEN` is set
- Verify token is a Page Access Token (not User Token)
- Check token hasn't expired
- Verify page permissions

#### Post Failed

- Check page permissions
- Verify you're an admin of the page
- Check API rate limits
- Verify content doesn't violate policies

### Instagram Issues

#### Authentication Failed

- Check `INSTAGRAM_ACCESS_TOKEN` is set
- Check `INSTAGRAM_ACCOUNT_ID` is set
- Verify account is a Business account
- Check token hasn't expired

#### Image URL Error

- Image must be publicly accessible
- Must use HTTPS (not HTTP)
- Image must be valid format (JPG, PNG)
- Check image URL is reachable

#### Post Failed

- Verify Business account is linked to Facebook page
- Check API rate limits
- Verify content doesn't violate policies
- Check image meets Instagram requirements

### Network Errors

- Check internet connection
- Verify Meta APIs are accessible
- Check firewall settings
- Verify no proxy issues

## Files

- **Script:** `scripts/post_meta.py`
- **Social Log:** `AI_Employee_Vault/Logs/social.log`
- **Business Log:** `AI_Employee_Vault/Logs/business.log`
- **Error Log:** `AI_Employee_Vault/Logs/error.log`

## API Reference

### post_facebook(content, link)

Posts to Facebook page.

**Parameters:**
- `content` (string): Post content
- `link` (string, optional): URL to share

**Returns:**
- Success: `{"success": true, "platform": "facebook", "post_id": "...", ...}`
- Error: `{"error": "error message"}`

### post_instagram(content, image_url)

Posts to Instagram.

**Parameters:**
- `content` (string): Post caption
- `image_url` (string): Publicly accessible image URL (required)

**Returns:**
- Success: `{"success": true, "platform": "instagram", "post_id": "...", ...}`
- Error: `{"error": "error message"}`

## Examples

### Simple Facebook Post

```bash
python scripts/post_meta.py facebook "Hello from AI Employee!"
```

### Facebook Post with Link

```bash
python scripts/post_meta.py facebook "Check out our blog!" "https://example.com/blog"
```

### Instagram Post

```bash
python scripts/post_meta.py instagram "Beautiful sunset! #nature" "https://example.com/sunset.jpg"
```

## Future Enhancements

- Video posting support
- Instagram Stories
- Facebook Stories
- Carousel posts (multiple images)
- Scheduled posts
- Post analytics
- Comment management
- Cross-posting (same content to both platforms)

## Status

✅ **Production Ready**
- Meta Graph API v18.0 integration
- Facebook page posting
- Instagram business posting
- Complete logging (social.log)
- Error handling
- Social summary integration
- Business log integration

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Operational ✅
