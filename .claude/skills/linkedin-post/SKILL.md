# LinkedIn Post Skill

## Purpose
Create real LinkedIn posts using browser automation with Playwright.

## Usage
Call this skill to create a text post on LinkedIn:
- Provide the post content/text
- The skill handles login and posting

## Requirements
- LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables must be set
- Playwright must be installed with Chromium
- Requires internet connection
- LinkedIn account access

## Instructions for Claude
To create a LinkedIn post, call the script with the post content as parameter. The skill will handle the browser automation to log in and create the post, returning success or error message.