# Business MCP Server - Quick Start

## Installation

```bash
# Navigate to the MCP directory
cd mcp/business_mcp

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Environment Setup

Create a `.env` file in the project root or set environment variables:

```bash
# Email credentials (Gmail)
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"

# LinkedIn credentials
export LINKEDIN_EMAIL="your-linkedin@email.com"
export LINKEDIN_PASSWORD="your-linkedin-password"
```

## Testing

Run the test suite:

```bash
python mcp/business_mcp/test_server.py
```

## Running the Server

```bash
python mcp/business_mcp/server.py
```

## Integration with Claude Desktop

Add to `~/.claude/config.json`:

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

## Usage Examples

Once configured with Claude Desktop, you can use natural language:

- "Send an email to client@example.com about the project update"
- "Post on LinkedIn about our new product launch"
- "Log this activity: Completed client onboarding"

All actions are automatically logged to `AI_Employee_Vault/Logs/business.log`.
