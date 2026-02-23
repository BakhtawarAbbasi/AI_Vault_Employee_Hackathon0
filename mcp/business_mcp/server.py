#!/usr/bin/env python3
"""
Business MCP Server
Provides external business actions for the AI Employee system.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Any, Sequence
import asyncio

# Email functionality
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# LinkedIn automation
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print(json.dumps({"error": "MCP SDK not installed. Run: pip install mcp"}))
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("business-mcp")

# Initialize MCP server
app = Server("business-mcp")

# Base path for vault
VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "AI_Employee_Vault")
LOGS_PATH = os.path.join(VAULT_PATH, "Logs")
os.makedirs(LOGS_PATH, exist_ok=True)


def log_activity(message: str) -> dict:
    """Log business activity to AI_Employee_Vault/Logs/business.log"""
    try:
        log_file = os.path.join(LOGS_PATH, "business.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        return {
            "success": True,
            "message": "Activity logged successfully",
            "log_file": log_file
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def send_email_sync(to: str, subject: str, body: str) -> dict:
    """Send email via SMTP (Gmail)"""
    try:
        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_PASSWORD')

        if not email_address or not email_password:
            return {
                "success": False,
                "error": "EMAIL_ADDRESS and EMAIL_PASSWORD environment variables must be set"
            }

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.send_message(msg)

        # Log the activity
        log_activity(f"Email sent to {to} with subject: {subject}")

        return {
            "success": True,
            "message": f"Email sent successfully to {to}",
            "to": to,
            "subject": subject
        }
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        log_activity(f"ERROR: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


async def post_linkedin_async(content: str) -> dict:
    """Create LinkedIn post via browser automation"""
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "success": False,
            "error": "Playwright not installed. Run: pip install playwright && playwright install"
        }

    try:
        linkedin_email = os.getenv('LINKEDIN_EMAIL')
        linkedin_password = os.getenv('LINKEDIN_PASSWORD')

        if not linkedin_email or not linkedin_password:
            return {
                "success": False,
                "error": "LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables must be set"
            }

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Login to LinkedIn
            await page.goto('https://www.linkedin.com/login')
            await page.fill('input[name="session_key"]', linkedin_email)
            await page.fill('input[name="session_password"]', linkedin_password)
            await page.click('button[type="submit"]')
            await page.wait_for_load_state('networkidle')

            # Navigate to feed
            await page.goto('https://www.linkedin.com/feed/')
            await page.wait_for_load_state('networkidle')

            # Click "Start a post" button
            await page.click('button[aria-label="Start a post"]')
            await page.wait_for_timeout(2000)

            # Fill in post content
            await page.fill('div[role="textbox"]', content)
            await page.wait_for_timeout(1000)

            # Click Post button
            await page.click('button[aria-label="Post"]')
            await page.wait_for_timeout(3000)

            await browser.close()

        # Log the activity
        log_activity(f"LinkedIn post created: {content[:50]}...")

        return {
            "success": True,
            "message": "LinkedIn post created successfully",
            "content_preview": content[:100]
        }
    except Exception as e:
        error_msg = f"Failed to create LinkedIn post: {str(e)}"
        log_activity(f"ERROR: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available business action tools"""
    return [
        Tool(
            name="send_email",
            description="Send an email via SMTP (Gmail). Requires EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content"
                    }
                },
                "required": ["to", "subject", "body"]
            }
        ),
        Tool(
            name="post_linkedin",
            description="Create a LinkedIn post via browser automation. Requires LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Content of the LinkedIn post"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="log_activity",
            description="Log business activity to AI_Employee_Vault/Logs/business.log",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Activity message to log"
                    }
                },
                "required": ["message"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls"""
    try:
        if name == "send_email":
            result = send_email_sync(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"]
            )
        elif name == "post_linkedin":
            result = await post_linkedin_async(content=arguments["content"])
        elif name == "log_activity":
            result = log_activity(message=arguments["message"])
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
