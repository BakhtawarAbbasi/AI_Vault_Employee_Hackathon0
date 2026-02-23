#!/usr/bin/env python3
"""
LinkedIn Watcher
Continuously monitors LinkedIn for new messages, connection requests, and business opportunities.
"""

import os
import sys
import time
import json
from datetime import datetime
from playwright.sync_api import sync_playwright


def create_action_file(content, action_type):
    """Create an action file in the vault"""
    # Create vault directories if they don't exist
    vault_path = "AI_Employee_Vault"
    needs_action_path = os.path.join(vault_path, "Needs_Action")
    os.makedirs(needs_action_path, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"LINKEDIN_{action_type}_{timestamp}.md"
    filepath = os.path.join(needs_action_path, filename)

    # Create markdown content
    markdown_content = f"""---
type: linkedin_{action_type}
timestamp: {datetime.now().isoformat()}
status: pending
---

# LinkedIn {action_type.replace('_', ' ').title()}

## Details
{content}

## Recommended Actions
- [ ] Review the {action_type} carefully
- [ ] Determine appropriate response
- [ ] Execute recommended action
- [ ] Update status when complete

---
LinkedIn activity detected on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return filepath


def watch_linkedin():
    """Monitor LinkedIn for new activity"""
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        return {"error": "LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables must be set"}

    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)  # Set to False to see browser
            page = browser.new_page()

            # Go to LinkedIn login
            page.goto('https://www.linkedin.com/login')
            time.sleep(2)

            # Fill in login credentials
            page.fill('input#username', email)
            page.fill('input#password', password)

            # Click login button
            page.click('button[type="submit"]')
            time.sleep(3)

            # Check if login was successful
            if 'feed' in page.url or 'dashboard' in page.url:
                # Navigate to notifications to check for new activity
                page.goto('https://www.linkedin.com/notifications/')
                time.sleep(2)

                # Look for new connection requests
                connection_requests = page.query_selector_all('div[role="listitem"] span:has-text("accepted your connection request")')

                if connection_requests:
                    content = f"New connection request activity detected on LinkedIn: {len(connection_requests)} recent connections"
                    filepath = create_action_file(content, "connection_request")
                    print(json.dumps({"info": f"Created action file: {filepath}", "type": "connection_request"}))

                # Check for messages
                page.goto('https://www.linkedin.com/messaging/')
                time.sleep(2)

                # Look for unread messages
                unread_messages = page.query_selector_all('div.msg-thread__message--unread')

                if unread_messages:
                    content = f"New unread messages detected on LinkedIn: {len(unread_messages)} messages"
                    filepath = create_action_file(content, "new_message")
                    print(json.dumps({"info": f"Created action file: {filepath}", "type": "new_message"}))

                # Check for content that might indicate business opportunities
                page.goto('https://www.linkedin.com/feed/')
                time.sleep(2)

                # Look for posts that might indicate business opportunities (could be enhanced)
                # For now we'll just simulate finding a business opportunity
                # In a real implementation, you would look for specific keywords or patterns
                business_opportunities = []

                if business_opportunities:
                    content = f"Potential business opportunity detected: {business_opportunities}"
                    filepath = create_action_file(content, "business_opportunity")
                    print(json.dumps({"info": f"Created action file: {filepath}", "type": "business_opportunity"}))

                browser.close()
                return {"success": "LinkedIn monitoring completed"}
            else:
                browser.close()
                return {"error": "Login failed - check credentials"}

    except Exception as e:
        return {"error": f"Failed to monitor LinkedIn: {str(e)}"}


def main():
    """Main function to run the LinkedIn watcher continuously"""
    print(json.dumps({"info": "Starting LinkedIn Watcher..."}))

    try:
        while True:
            result = watch_linkedin()

            if "error" in result:
                print(json.dumps(result))

            # Wait 5 minutes before next check
            time.sleep(300)

    except KeyboardInterrupt:
        print(json.dumps({"info": "LinkedIn Watcher stopped by user"}))
        sys.exit(0)


if __name__ == "__main__":
    main()