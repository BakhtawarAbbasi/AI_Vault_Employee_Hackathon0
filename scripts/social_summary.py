#!/usr/bin/env python3
"""
Social Summary System
Logs all social media activity to centralized Social_Log.md file
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re


# Configuration
VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "AI_Employee_Vault")
REPORTS_PATH = os.path.join(VAULT_PATH, "Reports")
SOCIAL_LOG = os.path.join(REPORTS_PATH, "Social_Log.md")
LOGS_PATH = os.path.join(VAULT_PATH, "Logs")

# Environment variables
AUTO_LOG = os.getenv('SOCIAL_SUMMARY_AUTO_LOG', 'true').lower() == 'true'
TRACK_ENGAGEMENT = os.getenv('SOCIAL_SUMMARY_TRACK_ENGAGEMENT', 'true').lower() == 'true'
CEO_INTEGRATION = os.getenv('SOCIAL_SUMMARY_CEO_INTEGRATION', 'true').lower() == 'true'


def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(REPORTS_PATH, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)


def log_to_business_log(message):
    """Log to business.log"""
    try:
        business_log = os.path.join(LOGS_PATH, "business.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] SOCIAL: {message}\n"

        with open(business_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass


def initialize_social_log():
    """Initialize Social_Log.md if it doesn't exist"""
    if not os.path.exists(SOCIAL_LOG):
        now = datetime.now()
        month_name = now.strftime("%B %Y")

        content = f"""# Social Media Activity Log

Last updated: {now.strftime("%Y-%m-%d %H:%M:%S")}

---

## {month_name}

### Week {get_week_number(now)} ({get_week_range_str(now)})

---

## Summary Statistics

### This Week
- Total Posts: 0
- LinkedIn: 0
- Facebook: 0
- Instagram: 0
- Twitter: 0
- Total Engagement: 0 interactions

### This Month
- Total Posts: 0
- LinkedIn: 0
- Facebook: 0
- Instagram: 0
- Twitter: 0
- Total Engagement: 0 interactions

---

*Maintained by Social Summary System*
"""

        with open(SOCIAL_LOG, 'w', encoding='utf-8') as f:
            f.write(content)

        log_to_business_log("Initialized Social_Log.md")


def get_week_number(date):
    """Get week number within the month"""
    first_day = date.replace(day=1)
    days_offset = (date - first_day).days
    week_num = (days_offset // 7) + 1
    return week_num


def get_week_range_str(date):
    """Get week range string (e.g., 'Feb 17-23')"""
    # Find Monday of current week
    days_since_monday = date.weekday()
    week_start = date - timedelta(days=days_since_monday)
    week_end = week_start + timedelta(days=6)

    return f"{week_start.strftime('%b %d')}-{week_end.strftime('%d')}"


def parse_social_log():
    """Parse Social_Log.md and extract posts"""
    if not os.path.exists(SOCIAL_LOG):
        return []

    posts = []

    with open(SOCIAL_LOG, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract posts using regex
    post_pattern = r'\*\*(\w+) Post\*\*\n- Time: ([\d:]+)\n- Content: (.+?)\n'
    matches = re.finditer(post_pattern, content)

    for match in matches:
        platform = match.group(1).lower()
        time = match.group(2)
        content_text = match.group(3)

        posts.append({
            'platform': platform,
            'time': time,
            'content': content_text
        })

    return posts


def log_post(platform, content, date=None, engagement=None, url=None):
    """Log a social media post"""
    ensure_directories()
    initialize_social_log()

    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    # Read existing log
    with open(SOCIAL_LOG, 'r', encoding='utf-8') as f:
        log_content = f.read()

    # Create post entry
    time_str = date.strftime('%H:%M:%S')
    date_str = date.strftime('%Y-%m-%d')

    # Truncate content if too long
    content_preview = content[:100] + '...' if len(content) > 100 else content

    post_entry = f"""
#### {date_str}

**{platform.title()} Post**
- Time: {time_str}
- Content: {content_preview}
"""

    if engagement and TRACK_ENGAGEMENT:
        if isinstance(engagement, dict):
            engagement_str = f"{engagement.get('likes', 0)} likes, {engagement.get('comments', 0)} comments"
            if 'shares' in engagement:
                engagement_str += f", {engagement['shares']} shares"
        else:
            engagement_str = str(engagement)
        post_entry += f"- Engagement: {engagement_str}\n"

    if url:
        post_entry += f"- URL: {url}\n"

    # Find the right place to insert (after the week header)
    week_header = f"### Week {get_week_number(date)} ({get_week_range_str(date)})"

    if week_header in log_content:
        # Insert after week header
        parts = log_content.split(week_header, 1)
        updated_content = parts[0] + week_header + post_entry + parts[1]
    else:
        # Add new week section
        month_header = f"## {date.strftime('%B %Y')}"
        if month_header in log_content:
            parts = log_content.split(month_header, 1)
            new_week_section = f"\n\n{week_header}{post_entry}\n"
            updated_content = parts[0] + month_header + new_week_section + parts[1]
        else:
            # Add new month section
            updated_content = log_content.replace(
                "---\n\n## Summary Statistics",
                f"\n## {date.strftime('%B %Y')}\n\n{week_header}{post_entry}\n\n---\n\n## Summary Statistics"
            )

    # Update timestamp
    updated_content = re.sub(
        r'Last updated: .*',
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        updated_content
    )

    # Write back
    with open(SOCIAL_LOG, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    # Update statistics
    update_statistics()

    # Log to business.log
    log_to_business_log(f"Logged {platform} post: {content_preview}")

    return {
        'success': True,
        'message': 'Social media post logged successfully',
        'platform': platform,
        'date': date_str
    }


def update_statistics():
    """Update summary statistics in Social_Log.md"""
    if not os.path.exists(SOCIAL_LOG):
        return

    posts = parse_social_log()

    # Count by platform
    platform_counts = {}
    for post in posts:
        platform = post['platform']
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

    # Calculate weekly and monthly stats
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    month_start = now.replace(day=1)

    # For simplicity, use total counts (in real implementation, filter by date)
    total_posts = len(posts)

    # Read log
    with open(SOCIAL_LOG, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update statistics section
    stats_section = f"""## Summary Statistics

### This Week
- Total Posts: {total_posts}
- LinkedIn: {platform_counts.get('linkedin', 0)}
- Facebook: {platform_counts.get('facebook', 0)}
- Instagram: {platform_counts.get('instagram', 0)}
- Twitter: {platform_counts.get('twitter', 0)}
- Total Engagement: 0 interactions

### This Month
- Total Posts: {total_posts}
- LinkedIn: {platform_counts.get('linkedin', 0)}
- Facebook: {platform_counts.get('facebook', 0)}
- Instagram: {platform_counts.get('instagram', 0)}
- Twitter: {platform_counts.get('twitter', 0)}
- Total Engagement: 0 interactions

---

*Maintained by Social Summary System*"""

    # Replace statistics section
    updated_content = re.sub(
        r'## Summary Statistics.*$',
        stats_section,
        content,
        flags=re.DOTALL
    )

    with open(SOCIAL_LOG, 'w', encoding='utf-8') as f:
        f.write(updated_content)


def view_log():
    """View the social log"""
    if not os.path.exists(SOCIAL_LOG):
        initialize_social_log()

    with open(SOCIAL_LOG, 'r', encoding='utf-8') as f:
        content = f.read()

    print(content)

    return {
        'success': True,
        'message': 'Social log displayed'
    }


def generate_summary(period='week'):
    """Generate social media summary"""
    ensure_directories()
    initialize_social_log()

    posts = parse_social_log()

    # Calculate date range
    now = datetime.now()
    if period == 'day':
        start_date = now.replace(hour=0, minute=0, second=0)
        period_str = now.strftime('%B %d, %Y')
    elif period == 'week':
        start_date = now - timedelta(days=now.weekday())
        end_date = start_date + timedelta(days=6)
        period_str = f"Week of {start_date.strftime('%b %d')}-{end_date.strftime('%d, %Y')}"
    elif period == 'month':
        start_date = now.replace(day=1)
        period_str = now.strftime('%B %Y')
    else:
        start_date = now - timedelta(days=7)
        period_str = 'Last 7 days'

    # Count posts by platform
    platform_counts = {}
    for post in posts:
        platform = post['platform']
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

    total_posts = len(posts)

    return {
        'success': True,
        'period': period_str,
        'total_posts': total_posts,
        'by_platform': {
            'linkedin': platform_counts.get('linkedin', 0),
            'facebook': platform_counts.get('facebook', 0),
            'instagram': platform_counts.get('instagram', 0),
            'twitter': platform_counts.get('twitter', 0)
        },
        'total_engagement': 0,  # Would be calculated from actual engagement data
        'average_engagement': 0.0
    }


def get_social_activity(start_date, end_date):
    """Get social activity for date range (for CEO briefing integration)"""
    posts = parse_social_log()

    # Filter by date range (simplified - in real implementation, parse dates from log)
    platform_counts = {}
    for post in posts:
        platform = post['platform']
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

    return {
        'total_posts': len(posts),
        'linkedin_posts': platform_counts.get('linkedin', 0),
        'facebook_posts': platform_counts.get('facebook', 0),
        'instagram_posts': platform_counts.get('instagram', 0),
        'twitter_posts': platform_counts.get('twitter', 0),
        'total_engagement': 0  # Would be calculated from actual engagement data
    }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Social Summary System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Log post
    log_parser = subparsers.add_parser('log', help='Log social media post')
    log_parser.add_argument('--platform', required=True, choices=['linkedin', 'facebook', 'instagram', 'twitter'], help='Social media platform')
    log_parser.add_argument('--content', required=True, help='Post content')
    log_parser.add_argument('--date', help='Post date (YYYY-MM-DD)')
    log_parser.add_argument('--engagement', help='Engagement metrics (JSON)')
    log_parser.add_argument('--url', help='Post URL')

    # View log
    subparsers.add_parser('view', help='View social log')

    # Generate summary
    summary_parser = subparsers.add_parser('summary', help='Generate summary')
    summary_parser.add_argument('--period', choices=['day', 'week', 'month'], default='week', help='Summary period')

    args = parser.parse_args()

    if args.command == 'log':
        engagement = json.loads(args.engagement) if args.engagement else None
        result = log_post(args.platform, args.content, args.date, engagement, args.url)
    elif args.command == 'view':
        result = view_log()
    elif args.command == 'summary':
        result = generate_summary(args.period)
    else:
        parser.print_help()
        return

    if args.command != 'view':  # view already prints content
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
