# Human Approval Skill

## Purpose
Implement human-in-the-loop approval for sensitive actions.

## Usage
- Create approval request in AI_Employee_Vault/Needs_Approval/
- Wait for human to mark as APPROVED or REJECTED
- Return final status

## Process
1. Create request file with action details
2. Monitor file for approval status
3. Return APPROVED, REJECTED, or timeout
4. Clean up request file after decision

## Instructions for Claude
To request approval, call the script with action details. The skill will create the request and wait for human decision, returning the final status.