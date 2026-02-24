#!/usr/bin/env python3
"""
Twitter Post Script
Post tweets using Twitter API v2 and log to history
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TwitterPoster:
    """Handle Twitter posting and logging"""

    def __init__(self):
        """Initialize Twitter API credentials"""
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_secret = os.getenv('TWITTER_ACCESS_SECRET')

        if not all([self.bearer_token, self.api_key, self.api_secret,
                   self.access_token, self.access_secret]):
            logger.warning("Twitter API credentials not fully configured")

        self.api_url = "https://api.twitter.com/2/tweets"

    def post_tweet(self, content: str) -> dict:
        """
        Post a tweet to Twitter

        Args:
            content: Tweet content (max 280 characters)

        Returns:
            Dict with success status and tweet details
        """
        try:
            # Validate content length
            if len(content) > 280:
                return {
                    "error": f"Tweet too long: {len(content)} characters (max 280)"
                }

            if not content.strip():
                return {"error": "Tweet content cannot be empty"}

            # Check credentials
            if not self.bearer_token:
                return {"error": "TWITTER_BEARER_TOKEN not set"}

            # Prepare request
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "text": content
            }

            # Post tweet
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 201:
                tweet_data = response.json()
                tweet_id = tweet_data['data']['id']
                tweet_text = tweet_data['data']['text']

                # Log to history
                self._log_to_history(tweet_id, tweet_text)

                # Log to business log
                self._log_business_activity(f"Posted tweet: {tweet_text[:50]}...")

                # Log to social summary
                self._log_to_social_summary(tweet_text)

                logger.info(f"Tweet posted successfully: {tweet_id}")

                return {
                    "success": True,
                    "tweet_id": tweet_id,
                    "content": tweet_text,
                    "url": f"https://twitter.com/user/status/{tweet_id}"
                }

            else:
                error_msg = f"Twitter API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                self._log_error(error_msg)
                return {"error": error_msg}

        except requests.exceptions.Timeout:
            error_msg = "Request timeout - Twitter API not responding"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except Exception as e:
            error_msg = f"Failed to post tweet: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def _log_to_history(self, tweet_id: str, content: str):
        """Log tweet to history file"""
        try:
            # Create reports directory if needed
            reports_dir = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Reports'
            reports_dir.mkdir(parents=True, exist_ok=True)

            history_file = reports_dir / 'Twitter_History.md'

            # Read existing content
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            else:
                existing_content = "# Twitter Post History\n\n"

            # Get current date info
            now = datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')
            month_year = now.strftime('%B %Y')

            # Check if we need to add month header
            if f"## {month_year}" not in existing_content:
                # Add new month section at the top (after title)
                lines = existing_content.split('\n')
                title = lines[0]
                rest = '\n'.join(lines[1:])
                existing_content = f"{title}\n\n## {month_year}\n{rest}"

            # Add new tweet entry
            tweet_entry = f"""
### {date_str} at {time_str}

**Tweet ID:** {tweet_id}
**Content:** {content}
**URL:** https://twitter.com/user/status/{tweet_id}

---
"""

            # Insert after month header
            lines = existing_content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith(f"## {month_year}"):
                    insert_index = i + 1
                    break

            lines.insert(insert_index, tweet_entry)
            new_content = '\n'.join(lines)

            # Write back
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            logger.info(f"Logged tweet to history: {history_file}")

        except Exception as e:
            logger.error(f"Failed to log to history: {e}")

    def _log_business_activity(self, message: str):
        """Log to business log"""
        try:
            log_dir = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'business.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] TWITTER: {message}\n")

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
                f.write(f"[{timestamp}] TWITTER_ERROR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")

    def _log_to_social_summary(self, content: str):
        """Log to social summary system"""
        try:
            import subprocess
            script_path = Path(__file__).parent.parent.parent / 'scripts' / 'social_summary.py'

            if script_path.exists():
                subprocess.run([
                    sys.executable,
                    str(script_path),
                    'log',
                    '--platform', 'twitter',
                    '--content', content,
                    '--date', datetime.now().strftime('%Y-%m-%d')
                ], check=False, capture_output=True)

        except Exception as e:
            logger.error(f"Failed to log to social summary: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python post_twitter.py <tweet_content>"}))
        sys.exit(1)

    content = ' '.join(sys.argv[1:])

    poster = TwitterPoster()
    result = poster.post_tweet(content)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
