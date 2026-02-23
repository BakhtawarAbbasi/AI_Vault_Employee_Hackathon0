# Task Planner

## Description
The Task Planner skill reads incoming tasks from the Inbox and creates structured execution plans. It analyzes the task requirements, breaks them into actionable steps, assigns appropriate priority levels, determines if human approval is needed, and saves a comprehensive Plan.md file to the Needs_Action folder.

## Purpose
To provide systematic and thorough planning for incoming tasks, ensuring all requirements are understood and a clear execution path is established before work begins.

## Workflow

### 1. Read Task
- Access the Inbox folder to identify new .md task files
- Read the complete content of each task file
- Parse title, description, requirements, and any existing checklists
- Extract all relevant information and context from the original task

### 2. Analyze Intent
- Determine the primary objective of the task
- Identify the expected deliverable or outcome
- Understand specific requirements and constraints
- Assess the scope and complexity of the work
- Identify any dependencies or prerequisites

### 3. Break into Steps
- Decompose the task into specific, actionable steps
- Organize steps in logical sequence for efficient execution
- Include both main steps and potential sub-steps
- Consider potential challenges and required resources for each step
- Ensure steps are granular enough to be actionable but not overly detailed

### 4. Assign Priority
- Evaluate urgency and importance relative to other tasks
- Consider impact on business objectives and deadlines
- Classify as: High (immediate attention required), Medium (standard priority), or Low (can be scheduled)
- Take into account resource availability and dependencies
- Adjust based on critical path considerations

### 5. Check if Human Approval Needed
- Determine if the task involves sensitive information or operations
- Assess if decisions require explicit human authorization
- Identify if budget, legal, or compliance implications exist
- Evaluate if the outcome has significant business impact requiring oversight
- Flag for approval if safety, security, or ethical considerations apply

### 6. Save Plan.md to Needs_Action
- Format the plan using the standard template with all required sections
- Include the original task content for reference
- Ensure all analytical results are clearly documented
- Save to the Needs_Action folder with timestamped filename
- Add metadata including creation time and original file reference

## Template Structure
Each plan follows the standardized format:
- Original Task (verbatim inclusion)
- Objective (clear statement of purpose)
- Step-by-Step Plan (detailed execution steps)
- Priority (High/Medium/Low classification)
- Requires Human Approval? (Yes/No with reasoning)
- Suggested Output (expected results)

## Guidelines
- Maintain consistency in plan structure and terminology
- Ensure plans are clear, actionable, and comprehensive
- Consider resource constraints and potential obstacles
- Include validation steps to confirm successful completion
- Balance thoroughness with efficiency to avoid over-planning