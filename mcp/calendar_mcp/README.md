# Calendar MCP Server

## Overview

MCP Server for calendar management with local JSON storage.

## Features

- **Create Events**: Schedule meetings, appointments, and reminders
- **List Events**: View events with date filtering
- **Update Events**: Modify existing events
- **Delete Events**: Remove events
- **Get Upcoming**: Quick view of upcoming events

## Installation

### Prerequisites

```bash
# Python 3.13+ required
python --version
```

### Setup

No additional dependencies required - uses Python standard library only.

## Usage

### Create Event

```bash
python mcp/calendar_mcp/server.py create_event '{
  "title": "Client Meeting",
  "start_time": "2026-02-25T14:00:00",
  "end_time": "2026-02-25T15:00:00",
  "description": "Discuss Q1 project deliverables",
  "location": "Conference Room A",
  "attendees": ["client@example.com", "team@example.com"]
}'
```

**Response:**
```json
{
  "success": true,
  "event_id": "event_1_1708768800",
  "title": "Client Meeting",
  "start_time": "2026-02-25T14:00:00",
  "end_time": "2026-02-25T15:00:00",
  "message": "Event created successfully"
}
```

### List Events

```bash
# List all events
python mcp/calendar_mcp/server.py list_events '{}'

# List events in date range
python mcp/calendar_mcp/server.py list_events '{
  "start_date": "2026-02-24T00:00:00",
  "end_date": "2026-02-28T23:59:59",
  "limit": 20
}'
```

**Response:**
```json
{
  "success": true,
  "events": [
    {
      "id": "event_1_1708768800",
      "title": "Client Meeting",
      "start_time": "2026-02-25T14:00:00",
      "end_time": "2026-02-25T15:00:00",
      "description": "Discuss Q1 project deliverables",
      "location": "Conference Room A",
      "attendees": ["client@example.com"],
      "created": "2026-02-24T09:19:00",
      "status": "confirmed"
    }
  ],
  "count": 1
}
```

### Update Event

```bash
python mcp/calendar_mcp/server.py update_event '{
  "event_id": "event_1_1708768800",
  "title": "Client Meeting - Updated",
  "location": "Conference Room B"
}'
```

**Response:**
```json
{
  "success": true,
  "event_id": "event_1_1708768800",
  "message": "Event updated successfully"
}
```

### Delete Event

```bash
python mcp/calendar_mcp/server.py delete_event '{
  "event_id": "event_1_1708768800"
}'
```

**Response:**
```json
{
  "success": true,
  "event_id": "event_1_1708768800",
  "message": "Event deleted successfully"
}
```

### Get Upcoming Events

```bash
# Get events for next 7 days (default)
python mcp/calendar_mcp/server.py get_upcoming '{}'

# Get events for next 30 days
python mcp/calendar_mcp/server.py get_upcoming '{
  "days": 30
}'
```

**Response:**
```json
{
  "success": true,
  "events": [...],
  "count": 5
}
```

## Integration with AI Employee

### Automatic Logging

All calendar operations are automatically logged to:
- `AI_Employee_Vault/Logs/business.log` - Successful operations
- `AI_Employee_Vault/Logs/error.log` - Errors and failures

### Data Storage

Calendar events are stored in:
- `AI_Employee_Vault/Calendar/events.json`

### Scheduler Integration

Add to `scripts/scheduler.py` for automated reminders:

```python
# Check upcoming events daily
scheduler.add_task(
    name="calendar_reminders",
    interval_seconds=86400,  # Daily
    command="mcp/calendar_mcp/server.py",
    args=["get_upcoming", '{"days": 1}']
)
```

## Error Handling

The server includes comprehensive error handling:
- Invalid date format validation
- End time must be after start time
- Event not found errors
- JSON parsing errors

All errors are logged and returned in a consistent format:

```json
{
  "error": "Error message description"
}
```

## Date Format

All dates must be in ISO 8601 format:
- Format: `YYYY-MM-DDTHH:MM:SS`
- Example: `2026-02-25T14:00:00`
- Timezone: Local time (no timezone offset)

## API Reference

### create_event(title, start_time, end_time, description, location, attendees)

Creates a new calendar event.

**Parameters:**
- `title` (string): Event title
- `start_time` (string): Start time in ISO format
- `end_time` (string): End time in ISO format
- `description` (string, optional): Event description
- `location` (string, optional): Event location
- `attendees` (array, optional): List of attendee emails

**Returns:** Event details or error

### list_events(start_date, end_date, limit)

Lists calendar events with optional filtering.

**Parameters:**
- `start_date` (string, optional): Filter events after this date
- `end_date` (string, optional): Filter events before this date
- `limit` (int, optional): Maximum events to return (default: 10)

**Returns:** List of events or error

### update_event(event_id, **kwargs)

Updates an existing calendar event.

**Parameters:**
- `event_id` (string): Event ID to update
- Any event field to update (title, start_time, end_time, etc.)

**Returns:** Success status or error

### delete_event(event_id)

Deletes a calendar event.

**Parameters:**
- `event_id` (string): Event ID to delete

**Returns:** Success status or error

### get_upcoming(days)

Gets upcoming events for the next N days.

**Parameters:**
- `days` (int, optional): Number of days to look ahead (default: 7)

**Returns:** List of upcoming events or error

## Use Cases

### Schedule Client Meeting

```bash
python mcp/calendar_mcp/server.py create_event '{
  "title": "Client A - Project Review",
  "start_time": "2026-02-26T10:00:00",
  "end_time": "2026-02-26T11:00:00",
  "description": "Review project progress and next steps",
  "location": "Zoom",
  "attendees": ["client@example.com"]
}'
```

### Schedule Personal Appointment

```bash
python mcp/calendar_mcp/server.py create_event '{
  "title": "Dentist Appointment",
  "start_time": "2026-02-27T15:00:00",
  "end_time": "2026-02-27T16:00:00",
  "location": "123 Main St"
}'
```

### Check Today's Schedule

```bash
python mcp/calendar_mcp/server.py list_events '{
  "start_date": "2026-02-24T00:00:00",
  "end_date": "2026-02-24T23:59:59"
}'
```

### View This Week's Events

```bash
python mcp/calendar_mcp/server.py get_upcoming '{
  "days": 7
}'
```

## Security

- All data stored locally
- No external API calls
- Complete audit trail
- No credentials required

## Future Enhancements

- Google Calendar API integration
- Recurring events support
- Event reminders/notifications
- Calendar sharing
- Time zone support
- Conflict detection
- Meeting room booking

## Troubleshooting

### Invalid Date Format

**Error:** `Invalid date format`

**Solution:** Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

### Event Not Found

**Error:** `Event not found: event_id`

**Solution:** Verify event ID exists using `list_events`

### End Time Before Start Time

**Error:** `End time must be after start time`

**Solution:** Ensure end_time is later than start_time

## Files

- **Server:** `mcp/calendar_mcp/server.py`
- **Config:** `mcp/calendar_mcp/mcp.json`
- **Data:** `AI_Employee_Vault/Calendar/events.json`
- **Business Log:** `AI_Employee_Vault/Logs/business.log`
- **Error Log:** `AI_Employee_Vault/Logs/error.log`

## Status

✅ **Production Ready**
- 5 actions implemented
- Complete error handling
- Business log integration
- Local JSON storage
- No external dependencies

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Operational ✅
