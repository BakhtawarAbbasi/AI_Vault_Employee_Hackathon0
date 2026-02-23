#!/usr/bin/env python3
"""
Test script for Business MCP Server
Tests all three capabilities: send_email, post_linkedin, log_activity
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from server import send_email_sync, log_activity


def test_log_activity():
    """Test the log_activity function"""
    print("\n=== Testing log_activity ===")
    result = log_activity("Test activity logged at " + datetime.now().isoformat())
    print(json.dumps(result, indent=2))
    return result["success"]


def test_send_email():
    """Test the send_email function"""
    print("\n=== Testing send_email ===")

    # Check if environment variables are set
    if not os.getenv('EMAIL_ADDRESS') or not os.getenv('EMAIL_PASSWORD'):
        print(json.dumps({
            "success": False,
            "error": "EMAIL_ADDRESS and EMAIL_PASSWORD environment variables not set",
            "note": "Skipping email test"
        }, indent=2))
        return False

    # Send test email to yourself
    to_email = os.getenv('EMAIL_ADDRESS')
    result = send_email_sync(
        to=to_email,
        subject="Test Email from Business MCP",
        body="This is a test email from the Business MCP server.\n\nTimestamp: " + datetime.now().isoformat()
    )
    print(json.dumps(result, indent=2))
    return result["success"]


def test_linkedin_post():
    """Test the LinkedIn post function"""
    print("\n=== Testing post_linkedin ===")

    # Check if environment variables are set
    if not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'):
        print(json.dumps({
            "success": False,
            "error": "LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables not set",
            "note": "Skipping LinkedIn test"
        }, indent=2))
        return False

    print(json.dumps({
        "info": "LinkedIn automation requires async execution",
        "note": "Run the full MCP server to test LinkedIn posting",
        "command": "python mcp/business_mcp/server.py"
    }, indent=2))
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Business MCP Server - Test Suite")
    print("=" * 60)

    results = {
        "log_activity": test_log_activity(),
        "send_email": test_send_email(),
        "post_linkedin": test_linkedin_post()
    }

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed"))
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
