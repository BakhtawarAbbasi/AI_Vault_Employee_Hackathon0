#!/usr/bin/env python3
"""
Meta Social Media Poster
Post to Facebook and Instagram using Meta Graph API
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


class MetaSocialPoster:
    """Handle Facebook and Instagram posting"""

    def __init__(self):
        """Initialize Meta API credentials"""
        self.facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.facebook_page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.instagram_account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
        self.instagram_access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')

        self.graph_api_url = "https://graph.facebook.com/v18.0"

    def post_facebook(self, content: str, link: str = None) -> dict:
        """
        Post to Facebook page

        Args:
            content: Post content
            link: Optional URL to share

        Returns:
            Dict with success status and post details
        """
        try:
            # Validate credentials
            if not self.facebook_access_token:
                return {"error": "FACEBOOK_ACCESS_TOKEN not set"}

            if not self.facebook_page_id:
                return {"error": "FACEBOOK_PAGE_ID not set"}

            if not content.strip():
                return {"error": "Post content cannot be empty"}

            # Prepare request
            url = f"{self.graph_api_url}/{self.facebook_page_id}/feed"

            params = {
                "message": content,
                "access_token": self.facebook_access_token
            }

            if link:
                params["link"] = link

            # Post to Facebook
            response = requests.post(url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                post_id = data.get('id')

                # Log to social.log
                self._log_to_social_log('facebook', content, post_id)

                # Log to business log
                self._log_business_activity(f"Posted to Facebook: {content[:50]}...")

                # Log to social summary
                self._log_to_social_summary('facebook', content)

                logger.info(f"Facebook post created: {post_id}")

                return {
                    "success": True,
                    "platform": "facebook",
                    "post_id": post_id,
                    "content": content,
                    "url": f"https://facebook.com/{post_id}"
                }

            else:
                error_msg = f"Facebook API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                self._log_error(error_msg)
                return {"error": error_msg}

        except requests.exceptions.Timeout:
            error_msg = "Request timeout - Facebook API not responding"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except Exception as e:
            error_msg = f"Failed to post to Facebook: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def post_instagram(self, content: str, image_url: str = None) -> dict:
        """
        Post to Instagram

        Args:
            content: Post caption
            image_url: URL of image to post (required for Instagram)

        Returns:
            Dict with success status and post details
        """
        try:
            # Validate credentials
            if not self.instagram_access_token:
                return {"error": "INSTAGRAM_ACCESS_TOKEN not set"}

            if not self.instagram_account_id:
                return {"error": "INSTAGRAM_ACCOUNT_ID not set"}

            if not content.strip():
                return {"error": "Post caption cannot be empty"}

            if not image_url:
                return {"error": "Instagram requires an image_url"}

            # Step 1: Create media container
            container_url = f"{self.graph_api_url}/{self.instagram_account_id}/media"

            container_params = {
                "image_url": image_url,
                "caption": content,
                "access_token": self.instagram_access_token
            }

            container_response = requests.post(
                container_url,
                params=container_params,
                timeout=30
            )

            if container_response.status_code != 200:
                error_msg = f"Instagram container error: {container_response.status_code} - {container_response.text}"
                logger.error(error_msg)
                self._log_error(error_msg)
                return {"error": error_msg}

            container_id = container_response.json().get('id')

            # Step 2: Publish media
            publish_url = f"{self.graph_api_url}/{self.instagram_account_id}/media_publish"

            publish_params = {
                "creation_id": container_id,
                "access_token": self.instagram_access_token
            }

            publish_response = requests.post(
                publish_url,
                params=publish_params,
                timeout=30
            )

            if publish_response.status_code == 200:
                data = publish_response.json()
                post_id = data.get('id')

                # Log to social.log
                self._log_to_social_log('instagram', content, post_id)

                # Log to business log
                self._log_business_activity(f"Posted to Instagram: {content[:50]}...")

                # Log to social summary
                self._log_to_social_summary('instagram', content)

                logger.info(f"Instagram post created: {post_id}")

                return {
                    "success": True,
                    "platform": "instagram",
                    "post_id": post_id,
                    "content": content,
                    "image_url": image_url
                }

            else:
                error_msg = f"Instagram publish error: {publish_response.status_code} - {publish_response.text}"
                logger.error(error_msg)
                self._log_error(error_msg)
                return {"error": error_msg}

        except requests.exceptions.Timeout:
            error_msg = "Request timeout - Instagram API not responding"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

        except Exception as e:
            error_msg = f"Failed to post to Instagram: {str(e)}"
            logger.error(error_msg)
            self._log_error(error_msg)
            return {"error": error_msg}

    def _log_to_social_log(self, platform: str, content: str, post_id: str):
        """Log to social.log"""
        try:
            log_dir = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'social.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {platform.upper()}: Posted - ID: {post_id} - Content: {content[:100]}...\n")

            logger.info(f"Logged to social.log: {platform}")

        except Exception as e:
            logger.error(f"Failed to log to social.log: {e}")

    def _log_business_activity(self, message: str):
        """Log to business log"""
        try:
            log_dir = Path(__file__).parent.parent.parent / 'AI_Employee_Vault' / 'Logs'
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / 'business.log'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] META_SOCIAL: {message}\n")

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
                f.write(f"[{timestamp}] META_SOCIAL_ERROR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")

    def _log_to_social_summary(self, platform: str, content: str):
        """Log to social summary system"""
        try:
            import subprocess
            script_path = Path(__file__).parent.parent.parent / 'scripts' / 'social_summary.py'

            if script_path.exists():
                subprocess.run([
                    sys.executable,
                    str(script_path),
                    'log',
                    '--platform', platform,
                    '--content', content,
                    '--date', datetime.now().strftime('%Y-%m-%d')
                ], check=False, capture_output=True)

        except Exception as e:
            logger.error(f"Failed to log to social summary: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: python post_meta.py <platform> <content> [image_url]"
        }))
        sys.exit(1)

    platform = sys.argv[1].lower()
    content = sys.argv[2]
    image_url = sys.argv[3] if len(sys.argv) > 3 else None

    poster = MetaSocialPoster()

    if platform == 'facebook':
        result = poster.post_facebook(content, link=image_url)
    elif platform == 'instagram':
        result = poster.post_instagram(content, image_url=image_url)
    else:
        result = {"error": f"Unknown platform: {platform}. Use 'facebook' or 'instagram'"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
