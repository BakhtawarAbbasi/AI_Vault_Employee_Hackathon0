# File Triage Skill

## Purpose
This skill enables the AI employee to read, analyze, and categorize incoming tasks from the Inbox folder, determining whether they require action or can be moved directly to Done.

## Step-by-Step Process

### 1. Reading a Task from Inbox
- Navigate to the Inbox folder
- Identify the newest .md file
- Open and read the entire content
- Extract key information from YAML frontmatter if present
- Identify the main task description and any checklist items

### 2. Summarizing the Task
- Identify the primary action requested
- Note any specific files or data mentioned
- List any prerequisites or dependencies
- Determine the expected outcome
- Create a brief summary in your working memory

### 3. Decision Framework: Needs Action vs. Done
- **Move to Needs_Action if:**
  - Task requires processing, analysis, or transformation of data
  - Task involves creating new content or files
  - Task requires external input or verification
  - Task is complex and requires multiple steps
  - Task has checklist items that are not completed

- **Move to Done if:**
  - Task is already completed (checklist items are marked as done)
  - Task is informational only with no required action
  - Task is a duplicate of a previously completed task
  - Task is unclear and requires human intervention
  - Task is outside the defined boundaries of the AI employee

### 4. Writing Output Markdown
- If task goes to Needs_Action:
  - Preserve original content
  - Add or update status field in YAML frontmatter to "pending"
  - Add a timestamp for when the task was triaged
  - Include any notes about the nature of work needed

- If task goes to Done:
  - Preserve original content
  - Update status field in YAML frontmatter to "completed"
  - Add completion timestamp
  - Add a note explaining why it was categorized as complete

### 5. Quality Control
- Verify that files are moved to the correct folder
- Ensure no original files are deleted from Inbox
- Confirm that all YAML frontmatter is properly formatted
- Check that timestamps follow consistent format (YYYY-MM-DD HH:MM:SS)

## Boundaries
- Do not modify content of original task files beyond adding status and timestamps
- Do not process files that are not .md format
- Do not make assumptions beyond the explicit content in the task file
