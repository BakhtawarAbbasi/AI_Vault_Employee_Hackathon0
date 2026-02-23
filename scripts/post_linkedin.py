#!/usr/bin/env python3
"""
LinkedIn Post Skill
Create real LinkedIn posts using browser automation with Playwright.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright


def post_linkedin(content):
    """Create a LinkedIn text post"""
    # Get credentials from environment variables
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        return {"error": "LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables must be set"}

    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False)  # Set to True for production
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

            # Check if login was successful by looking for the feed
            if 'feed' in page.url or 'dashboard' in page.url:
                # Find the post creation area
                # Look for the text area where you write posts
                try:
                    # Try different selectors for the post input area
                    post_selector = 'textarea[aria-label="Create a post"]'
                    page.wait_for_selector(post_selector, timeout=5000)
                    page.fill(post_selector, content)

                    # Try to find and click the post button
                    post_button_selector = 'button[aria-label="Share"]'
                    page.wait_for_selector(post_button_selector, timeout=5000)
                    page.click(post_button_selector)

                    # Wait a moment for the post to be submitted
                    time.sleep(2)

                    # Check if post appeared (basic verification)
                    if "Create a post" not in page.content():
                        browser.close()

                        # Log to social summary
                        try:
                            subprocess.run([
                                sys.executable,
                                os.path.join(os.path.dirname(__file__), 'social_summary.py'),
                                'log',
                                '--platform', 'linkedin',
                                '--content', content,
                                '--date', datetime.now().strftime('%Y-%m-%d')
                            ], check=False, capture_output=True)
                        except Exception:
                            pass  # Don't fail the post if logging fails

                        return {"success": f"LinkedIn post created successfully: {content[:50]}..."}
                    else:
                        browser.close()
                        return {"error": "Post may not have been created successfully"}

                except Exception as e:
                    browser.close()
                    return {"error": f"Failed to create post: {str(e)}"}
            else:
                browser.close()
                return {"error": "Login failed - check credentials"}

    except Exception as e:
        return {"error": f"Failed to post on LinkedIn: {str(e)}"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python post_linkedin.py <post_content>"}))
        sys.exit(1)

    content = ' '.join(sys.argv[1:])

    result = post_linkedin(content)
    print(json.dumps(result))


if __name__ == "__main__":
    main()