#!/usr/bin/env python3
"""
Human Approval Skill
Create approval requests and wait for human decision.
"""

import os
import sys
import json
import time
from datetime import datetime


def request_approval(action_type, details, timeout_minutes=60):
    """Create an approval request and wait for human decision"""
    # Create the approval request file
    base_path = "AI_Employee_Vault"
    approval_folder = os.path.join(base_path, "Needs_Approval")
    os.makedirs(approval_folder, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"approval_{action_type}_{timestamp}.md"
    filepath = os.path.join(approval_folder, filename)

    # Create approval request content
    approval_content = f"""# Approval Request

## Action Type
{action_type}

## Details
{details}

## Status
PENDING

## Requested at
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Decision Required
Please edit this file to indicate your decision:
- To approve: Change status to APPROVED
- To reject: Change status to REJECTED

After making your decision, save the file.
"""

    # Write the approval request file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(approval_content)

    print(json.dumps({"info": f"Approval request created: {filename}"}))

    # Wait for decision with timeout
    timeout_seconds = timeout_minutes * 60
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if status has been updated
            if 'APPROVED' in content.upper():
                # Clean up the file after approval
                os.remove(filepath)
                return {"status": "APPROVED", "message": f"Action {action_type} approved by human"}
            elif 'REJECTED' in content.upper():
                # Clean up the file after rejection
                os.remove(filepath)
                return {"status": "REJECTED", "message": f"Action {action_type} rejected by human"}

        except Exception as e:
            # If there's an issue reading the file, continue waiting
            pass

        time.sleep(5)  # Check every 5 seconds

    # Timeout occurred
    # Update file to indicate timeout
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add timeout notice to the file
        timeout_notice = f"\n\n## TIMEOUT\nThis request timed out after {timeout_minutes} minutes. Please recreate if still needed.\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content + timeout_notice)
    except:
        pass  # If we can't update the file, just continue

    return {"status": "TIMEOUT", "message": f"Approval timeout after {timeout_minutes} minutes"}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python request_approval.py <action_type> <details> [timeout_minutes]"}))
        sys.exit(1)

    action_type = sys.argv[1]
    details = ' '.join(sys.argv[2:-1] if len(sys.argv) > 3 else sys.argv[2:])
    timeout_minutes = int(sys.argv[-1]) if len(sys.argv) > 3 else 60

    result = request_approval(action_type, details, timeout_minutes)
    print(json.dumps(result))


if __name__ == "__main__":
    main()