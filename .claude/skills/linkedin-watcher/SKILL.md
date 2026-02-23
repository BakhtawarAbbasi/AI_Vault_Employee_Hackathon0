# LinkedIn Watcher Skill

## Purpose
Continuously monitor LinkedIn for new messages, connection requests, and business opportunities.

## Usage
Run as a background process that:
- Monitors LinkedIn for new activity
- Creates action files when relevant events occur
- Flags business opportunities for sales generation

## Requirements
- LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables
- Requires internet connection
- Playwright with Chromium browser

## Instructions for Claude
Run the script as a continuous monitoring process. The skill will watch for new LinkedIn activity and create markdown files in the vault when relevant events are detected.