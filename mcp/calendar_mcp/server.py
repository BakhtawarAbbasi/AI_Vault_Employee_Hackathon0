#!/usr/bin/env python3
"""
Calendar MCP Server
Provides calendar management integration via Google Calendar API
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CalendarMCPServer:
    """MCP Server for Calendar management"""

    def __init__(self):
        """Initialize Calendar MCP server"""
        self.calendar_file = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Calendar' / 'events.json'
        self.calendar_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize calendar file if it doesn't exist
        if not self.calendar_file.exists():
            self._initialize_calendar()

    def _initialize_calendar(self):
        """Initialize empty calendar file"""
        initial_data = {
            "events": [],
            "last_updated": datetime.now().isoformat()
        }
        with open(self.calendar_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2)

    def _load_calendar(self) -> Dict:
        """Load calendar data"""
        try:
            with open(self.calendar_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading calendar: {e}")
            return {"events": [], "last_updated": datetime.now().isoformat()}

    def _save_calendar(self, data: Dict):
        """Save calendar data"""
        try:
            data['last_updated'] = datetime.now().isoformat()
            with open(self.calendar_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving calendar: {e}")

    def create_event(self, title: str, start_time: str, end_time: str,
                    description: str = "", location: str = "",
                    attendees: List[str] = None) -> Dict[str, Any]:
        """
        Create a calendar event

        Args:
            title: Event title
            start_time: Start time (ISO format: YYYY-MM-DDTHH:MM:SS)
            end_time: End time (ISO format: YYYY-MM-DDTHH:MM:SS)
            description: Event description
            location: Event location
            attendees: List of attendee emails

        Returns:
            Dict with success status and event details
        """
        try:
            # Validate times
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)

            if end_dt <= start_dt:
                return {"error": "End time must be after start time"}

            # Load calendar
            calendar_data = self._load_calendar()

            # Generate event ID
            event_id = f"event_{len(calendar_data['events']) + 1}_{int(datetime.now().timestamp())}"

            # Create event
            event = {
                "id": event_id,
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
                "location": location,
                "attendees": attendees or [],
                "created": datetime.now().isoformat(),
                "status": "confirmed"
            }

            # Add to calendar
            calendar_data['events'].append(event)
            self._save_calendar(calendar_data)

            # Log to business log
            self._log_business_activity(
                f"Created calendar event: {title} on {start_time}"
            )

            logger.info(f"Created event: {event_id}")

            return {
                "success": True,
                "event_id": event_id,
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "message": "Event created successfully"
            }

        except ValueError as e:
            error_msg = f"Invalid date format: {e}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except Exception as e:
            error_msg = f"Failed to create event: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def list_events(self, start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   limit: int = 10) -> Dict[str, Any]:
        """
        List calendar events

        Args:
            start_date: Filter events after this date (ISO format)
            end_date: Filter events before this date (ISO format)
            limit: Maximum number of events to return

        Returns:
            Dict with success status and event list
        """
        try:
            calendar_data = self._load_calendar()
            events = calendar_data['events']

            # Filter by date range
            if start_date:
                start_dt = datetime.fromisoformat(start_date)
                events = [e for e in events if datetime.fromisoformat(e['start_time']) >= start_dt]

            if end_date:
                end_dt = datetime.fromisoformat(end_date)
                events = [e for e in events if datetime.fromisoformat(e['start_time']) <= end_dt]

            # Sort by start time
            events.sort(key=lambda e: e['start_time'])

            # Limit results
            events = events[:limit]

            logger.info(f"Retrieved {len(events)} events")

            return {
                "success": True,
                "events": events,
                "count": len(events)
            }

        except Exception as e:
            error_msg = f"Failed to list events: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def update_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update a calendar event

        Args:
            event_id: Event ID to update
            **kwargs: Fields to update (title, start_time, end_time, description, location, attendees)

        Returns:
            Dict with success status
        """
        try:
            calendar_data = self._load_calendar()

            # Find event
            event = None
            for e in calendar_data['events']:
                if e['id'] == event_id:
                    event = e
                    break

            if not event:
                return {"error": f"Event not found: {event_id}"}

            # Update fields
            for key, value in kwargs.items():
                if key in ['title', 'start_time', 'end_time', 'description', 'location', 'attendees']:
                    event[key] = value

            # Validate times if updated
            if 'start_time' in kwargs or 'end_time' in kwargs:
                start_dt = datetime.fromisoformat(event['start_time'])
                end_dt = datetime.fromisoformat(event['end_time'])
                if end_dt <= start_dt:
                    return {"error": "End time must be after start time"}

            event['updated'] = datetime.now().isoformat()

            # Save calendar
            self._save_calendar(calendar_data)

            # Log to business log
            self._log_business_activity(
                f"Updated calendar event: {event_id}"
            )

            logger.info(f"Updated event: {event_id}")

            return {
                "success": True,
                "event_id": event_id,
                "message": "Event updated successfully"
            }

        except Exception as e:
            error_msg = f"Failed to update event: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """
        Delete a calendar event

        Args:
            event_id: Event ID to delete

        Returns:
            Dict with success status
        """
        try:
            calendar_data = self._load_calendar()

            # Find and remove event
            original_count = len(calendar_data['events'])
            calendar_data['events'] = [e for e in calendar_data['events'] if e['id'] != event_id]

            if len(calendar_data['events']) == original_count:
                return {"error": f"Event not found: {event_id}"}

            # Save calendar
            self._save_calendar(calendar_data)

            # Log to business log
            self._log_business_activity(
                f"Deleted calendar event: {event_id}"
            )

            logger.info(f"Deleted event: {event_id}")

            return {
                "success": True,
                "event_id": event_id,
                "message": "Event deleted successfully"
            }

        except Exception as e:
            error_msg = f"Failed to delete event: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def get_upcoming_events(self, days: int = 7) -> Dict[str, Any]:
        """
        Get upcoming events for the next N days

        Args:
            days: Number of days to look ahead

        Returns:
            Dict with success status and upcoming events
        """
        try:
            start_date = datetime.now().isoformat()
            end_date = (datetime.now() + timedelta(days=days)).isoformat()

            return self.list_events(start_date=start_date, end_date=end_date, limit=50)

        except Exception as e:
            error_msg = f"Failed to get upcoming events: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def _log_business_activity(self, message: str):
        """Log to business log"""
        try:
            log_dir = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'business.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] CALENDAR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log business activity: {e}")

    def _log_error(self, message: str):
        """Log error"""
        try:
            log_dir = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'error.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] CALENDAR_ERROR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")

    def handle_request(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request"""
        try:
            if action == 'create_event':
                return self.create_event(
                    title=params.get('title'),
                    start_time=params.get('start_time'),
                    end_time=params.get('end_time'),
                    description=params.get('description', ''),
                    location=params.get('location', ''),
                    attendees=params.get('attendees', [])
                )

            elif action == 'list_events':
                return self.list_events(
                    start_date=params.get('start_date'),
                    end_date=params.get('end_date'),
                    limit=params.get('limit', 10)
                )

            elif action == 'update_event':
                event_id = params.pop('event_id', None)
                if not event_id:
                    return {"error": "event_id is required"}
                return self.update_event(event_id, **params)

            elif action == 'delete_event':
                return self.delete_event(
                    event_id=params.get('event_id')
                )

            elif action == 'get_upcoming':
                return self.get_upcoming_events(
                    days=params.get('days', 7)
                )

            else:
                return {"error": f"Unknown action: {action}"}

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {"error": str(e)}


def main():
    """Main entry point for MCP server"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python server.py <action> [params_json]"}))
        sys.exit(1)

    action = sys.argv[1]
    params = {}

    if len(sys.argv) > 2:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON parameters"}))
            sys.exit(1)

    server = CalendarMCPServer()
    result = server.handle_request(action, params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
