# Gmail Send Skill

## Purpose
Send real emails via Gmail SMTP using environment variables for authentication.

## Usage
Call this skill to send emails with:
- Recipient (to)
- Subject line
- Email body content

## Requirements
- EMAIL_ADDRESS and EMAIL_PASSWORD environment variables must be set
- Requires internet connection
- Uses Gmail SMTP settings

## Instructions for Claude
To send an email, call the script with recipient, subject, and body parameters. The skill will handle authentication and delivery, returning success or error message.