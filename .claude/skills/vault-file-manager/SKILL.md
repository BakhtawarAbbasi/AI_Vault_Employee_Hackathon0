# Vault File Manager Skill

## Purpose
Manage task workflow by moving files between vault folders.

## Usage
Move files between:
- AI_Employee_Vault/Inbox/
- AI_Employee_Vault/Needs_Action/
- AI_Employee_Vault/Done/

## Supported Operations
- Move task from Inbox to Needs_Action
- Move task from Needs_Action to Done
- Move task from Needs_Action back to Inbox (if needed)
- Any other valid combination

## Instructions for Claude
To move a file, call the script with source, destination, and filename. The skill will handle the file operation and return success or error message.