#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Summary Integration Test
Tests the complete social media logging workflow
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def test_social_summary_integration():
    """Test complete social summary integration"""
    print("=" * 60)
    print("SOCIAL SUMMARY INTEGRATION TEST")
    print("=" * 60)
    print()

    results = {
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "details": []
    }

    # Test 1: Log a LinkedIn post
    print("Test 1: Log LinkedIn Post")
    print("-" * 60)

    test_content = "Testing social summary integration - automated logging system"
    test_date = datetime.now().strftime('%Y-%m-%d')

    try:
        result = subprocess.run([
            sys.executable,
            'scripts/social_summary.py',
            'log',
            '--platform', 'linkedin',
            '--content', test_content,
            '--date', test_date
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout)

        if output.get('success'):
            print("✓ LinkedIn post logged successfully")
            results["tests_passed"] += 1
            results["details"].append({
                "test": "Log LinkedIn Post",
                "status": "PASSED",
                "message": "Post logged successfully"
            })
        else:
            print("✗ Failed to log LinkedIn post")
            results["tests_failed"] += 1
            results["details"].append({
                "test": "Log LinkedIn Post",
                "status": "FAILED",
                "message": "Post logging failed"
            })
    except Exception as e:
        print(f"✗ Exception: {e}")
        results["tests_failed"] += 1
        results["details"].append({
            "test": "Log LinkedIn Post",
            "status": "FAILED",
            "message": str(e)
        })

    results["tests_run"] += 1
    print()

    # Test 2: Verify Social_Log.md exists and contains entry
    print("Test 2: Verify Social_Log.md")
    print("-" * 60)

    social_log_path = Path("AI_Employee_Vault/Reports/Social_Log.md")

    try:
        if social_log_path.exists():
            with open(social_log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if test_content[:50] in content:
                print("✓ Social_Log.md contains the logged post")
                results["tests_passed"] += 1
                results["details"].append({
                    "test": "Verify Social_Log.md",
                    "status": "PASSED",
                    "message": "Log file contains entry"
                })
            else:
                print("✗ Social_Log.md does not contain the logged post")
                results["tests_failed"] += 1
                results["details"].append({
                    "test": "Verify Social_Log.md",
                    "status": "FAILED",
                    "message": "Log file missing entry"
                })
        else:
            print("✗ Social_Log.md does not exist")
            results["tests_failed"] += 1
            results["details"].append({
                "test": "Verify Social_Log.md",
                "status": "FAILED",
                "message": "Log file not found"
            })
    except Exception as e:
        print(f"✗ Exception: {e}")
        results["tests_failed"] += 1
        results["details"].append({
            "test": "Verify Social_Log.md",
            "status": "FAILED",
            "message": str(e)
        })

    results["tests_run"] += 1
    print()

    # Test 3: Generate weekly summary
    print("Test 3: Generate Weekly Summary")
    print("-" * 60)

    try:
        result = subprocess.run([
            sys.executable,
            'scripts/social_summary.py',
            'summary',
            '--period', 'week'
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout)

        if output.get('success') and output.get('total_posts', 0) > 0:
            print(f"✓ Weekly summary generated: {output['total_posts']} posts")
            print(f"  - LinkedIn: {output['by_platform']['linkedin']}")
            print(f"  - Period: {output['period']}")
            results["tests_passed"] += 1
            results["details"].append({
                "test": "Generate Weekly Summary",
                "status": "PASSED",
                "message": f"{output['total_posts']} posts found"
            })
        else:
            print("✗ Failed to generate weekly summary")
            results["tests_failed"] += 1
            results["details"].append({
                "test": "Generate Weekly Summary",
                "status": "FAILED",
                "message": "Summary generation failed"
            })
    except Exception as e:
        print(f"✗ Exception: {e}")
        results["tests_failed"] += 1
        results["details"].append({
            "test": "Generate Weekly Summary",
            "status": "FAILED",
            "message": str(e)
        })

    results["tests_run"] += 1
    print()

    # Test 4: Verify business.log integration
    print("Test 4: Verify Business Log Integration")
    print("-" * 60)

    business_log_path = Path("AI_Employee_Vault/Logs/business.log")

    try:
        if business_log_path.exists():
            with open(business_log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if "SOCIAL:" in content and "linkedin" in content.lower():
                print("✓ Business log contains social media activity")
                results["tests_passed"] += 1
                results["details"].append({
                    "test": "Verify Business Log Integration",
                    "status": "PASSED",
                    "message": "Business log integration working"
                })
            else:
                print("✗ Business log missing social media entries")
                results["tests_failed"] += 1
                results["details"].append({
                    "test": "Verify Business Log Integration",
                    "status": "FAILED",
                    "message": "No social entries in business log"
                })
        else:
            print("✗ business.log does not exist")
            results["tests_failed"] += 1
            results["details"].append({
                "test": "Verify Business Log Integration",
                "status": "FAILED",
                "message": "Business log not found"
            })
    except Exception as e:
        print(f"✗ Exception: {e}")
        results["tests_failed"] += 1
        results["details"].append({
            "test": "Verify Business Log Integration",
            "status": "FAILED",
            "message": str(e)
        })

    results["tests_run"] += 1
    print()

    # Test 5: Test multiple platform logging
    print("Test 5: Multi-Platform Logging")
    print("-" * 60)

    platforms = ['facebook', 'instagram', 'twitter']
    platform_tests_passed = 0

    for platform in platforms:
        try:
            result = subprocess.run([
                sys.executable,
                'scripts/social_summary.py',
                'log',
                '--platform', platform,
                '--content', f'Test post for {platform}',
                '--date', test_date
            ], capture_output=True, text=True, check=True)

            output = json.loads(result.stdout)

            if output.get('success'):
                print(f"✓ {platform.title()} post logged")
                platform_tests_passed += 1
            else:
                print(f"✗ {platform.title()} post failed")
        except Exception as e:
            print(f"✗ {platform.title()} exception: {e}")

    if platform_tests_passed == len(platforms):
        results["tests_passed"] += 1
        results["details"].append({
            "test": "Multi-Platform Logging",
            "status": "PASSED",
            "message": "All platforms logged successfully"
        })
    else:
        results["tests_failed"] += 1
        results["details"].append({
            "test": "Multi-Platform Logging",
            "status": "FAILED",
            "message": f"Only {platform_tests_passed}/{len(platforms)} platforms worked"
        })

    results["tests_run"] += 1
    print()

    # Print final results
    print("=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Tests Run: {results['tests_run']}")
    print(f"Tests Passed: {results['tests_passed']}")
    print(f"Tests Failed: {results['tests_failed']}")
    print(f"Success Rate: {(results['tests_passed']/results['tests_run']*100):.1f}%")
    print()

    if results['tests_failed'] == 0:
        print("✓ ALL TESTS PASSED")
        print()
        print("Social Summary Integration: OPERATIONAL ✓")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print()
        print("Failed Tests:")
        for detail in results['details']:
            if detail['status'] == 'FAILED':
                print(f"  - {detail['test']}: {detail['message']}")
        return 1


if __name__ == "__main__":
    sys.exit(test_social_summary_integration())
