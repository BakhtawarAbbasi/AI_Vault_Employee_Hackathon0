# Business MCP Server

A production-ready MCP (Model Context Protocol) server that provides external business actions for the AI Employee system.

## Features

This MCP server exposes three powerful business actions:

1. **send_email** - Send emails via SMTP (Gmail)
2. **post_linkedin** - Create LinkedIn posts via browser automation
3. **log_activity** - Log business activities to the vault

## Installation

### Prerequisites

```bash
# Install required Python packages
pip install mcp playwright

# Install Playwright browsers (required for LinkedIn automation)
playwright install
```

### Environment Variables

Create a `.env` file or set these environment variables:

```bash
# For email functionality
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# For LinkedIn functionality
LINKEDIN_EMAIL=your-linkedin@email.com
LINKEDIN_PASSWORD=your-linkedin-password
```

**Important**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## Usage

### Running the Server

```bash
python mcp/business_mcp/server.py
```

The server runs as an MCP stdio server and communicates via standard input/output.

### Configuring with Claude Desktop

Add this to your Claude Desktop configuration (`~/.claude/config.json` or `%APPDATA%\Claude\config.json` on Windows):

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

## Available Tools

### 1. send_email

Send an email via SMTP (Gmail).

**Parameters:**
- `to` (string, required) - Recipient email address
- `subject` (string, required) - Email subject line
- `body` (string, required) - Email body content

**Example:**
```json
{
  "to": "client@example.com",
  "subject": "Project Update",
  "body": "Hello, here is the latest update on your project..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully to client@example.com",
  "to": "client@example.com",
  "subject": "Project Update"
}
```

### 2. post_linkedin

Create a LinkedIn post via browser automation.

**Parameters:**
- `content` (string, required) - Content of the LinkedIn post

**Example:**
```json
{
  "content": "Excited to announce our new AI Employee system! It automates business tasks and increases efficiency. #AI #Automation"
}
```

**Response:**
```json
{
  "success": true,
  "message": "LinkedIn post created successfully",
  "content_preview": "Excited to announce our new AI Employee system! It automates business tasks and increases effic..."
}
```

**Note**: LinkedIn automation runs in non-headless mode so you can see the browser actions. This is intentional for security and verification purposes.

### 3. log_activity

Log business activity to `AI_Employee_Vault/Logs/business.log`.

**Parameters:**
- `message` (string, required) - Activity message to log

**Example:**
```json
{
  "message": "Completed client onboarding for Acme Corp"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Activity logged successfully",
  "log_file": "D:\\personal-ai-employee-hackathon\\AI_Employee_Vault\\Logs\\business.log"
}
```

## Log Format

All activities are automatically logged to `AI_Employee_Vault/Logs/business.log` with timestamps:

```
[2026-02-23 16:28:00] Email sent to client@example.com with subject: Project Update
[2026-02-23 16:30:15] LinkedIn post created: Excited to announce our new AI Employee system...
[2026-02-23 16:35:42] Completed client onboarding for Acme Corp
```

## Error Handling

All tools return structured error responses:

```json
{
  "success": false,
  "error": "Detailed error message here"
}
```

Common errors:
- Missing environment variables
- Invalid email credentials
- LinkedIn login failures
- Network connectivity issues

## Security Best Practices

1. **Never commit credentials** - Use environment variables only
2. **Use App Passwords** - For Gmail, generate an app-specific password
3. **Secure storage** - Store credentials in system environment or secure vault
4. **Log rotation** - Monitor `business.log` file size and rotate as needed
5. **Rate limiting** - Be mindful of API rate limits for email and LinkedIn

## Integration with AI Employee

This MCP server integrates seamlessly with the AI Employee system:

1. **Automated emails** - Send client updates, reports, notifications
2. **Social media presence** - Post business updates to LinkedIn
3. **Activity tracking** - All actions are logged for audit trail

### Example Workflow

```
Task in Inbox → Plan created → MCP actions executed → Results logged → Task moved to Done
```

## Troubleshooting

### Email not sending
- Verify EMAIL_ADDRESS and EMAIL_PASSWORD are set correctly
- For Gmail, ensure "Less secure app access" is enabled or use App Password
- Check firewall settings for SMTP port 587

### LinkedIn automation failing
- Ensure Playwright browsers are installed: `playwright install`
- LinkedIn may update their UI - selectors may need adjustment
- Check LINKEDIN_EMAIL and LINKEDIN_PASSWORD are correct
- LinkedIn may require 2FA - consider using session cookies instead

### Logs not appearing
- Verify `AI_Employee_Vault/Logs/` directory exists
- Check file permissions for write access
- Ensure path is correct relative to server.py location

## Development

### Project Structure
```
mcp/business_mcp/
├── server.py       # Main MCP server implementation
└── README.md       # This file
```

### Testing

Test individual functions:

```python
# Test email
python -c "from server import send_email_sync; print(send_email_sync('test@example.com', 'Test', 'Body'))"

# Test logging
python -c "from server import log_activity; print(log_activity('Test message'))"
```

## License

Part of the Personal AI Employee hackathon project.

## Support

For issues or questions, refer to the main project documentation or create an issue in the project repository.
