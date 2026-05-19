#!/usr/bin/env python3
"""
Canvas Page Synchronization CLI Tool

Sync markdown files between local canvas_pages/ folder and Canvas LMS.

Usage:
    python canvas_sync.py up [--course COURSE_ID] [--verbose]
    python canvas_sync.py down [--course COURSE_ID] [--verbose]

Commands:
    up      Upload all markdown files from canvas_pages/ to Canvas
    down    Download all Canvas pages to canvas_pages/ folder

Options:
    --course COURSE_ID    Override default course ID (default: 14011875)
    --verbose             Show detailed progress information

Examples:
    python canvas_sync.py up              Upload to default course
    python canvas_sync.py down --verbose  Download with progress info
    python canvas_sync.py up --course 123 Upload to specific course
    python canvas_sync.py --help          Show this help message
"""

import argparse
import sys
import os
from pathlib import Path

# Import canvastask module
try:
    import canvastask
except ImportError:
    print("Error: canvastask module not found")
    print("Make sure you're running from the code/ directory")
    sys.exit(1)

# Default configuration
DEFAULT_COURSE_ID = 14011875
DEFAULT_PAGES_DIR = 'canvas_pages'


def sync_up(course_id, pages_dir='canvas_pages', verbose=False):
    """Upload all markdown files to Canvas"""
    if verbose:
        print(f"Uploading markdown files from {pages_dir}/ to Canvas...")
        print(f"Course ID: {course_id}\n")

    try:
        canvastask.upload_all_markdown_files(
            course_id,
            canvas_folder=pages_dir,
            default_published=False
        )
        if verbose:
            print("\n[OK] Upload complete")
        return 0
    except Exception as e:
        print(f"[FAIL] Upload failed: {e}", file=sys.stderr)
        return 1


def sync_down(course_id, pages_dir='canvas_pages', verbose=False):
    """Download all Canvas pages to markdown"""
    if verbose:
        print(f"Downloading Canvas pages to {pages_dir}/...")
        print(f"Course ID: {course_id}\n")

    try:
        canvastask.download_canvas_pages_to_markdown(
            course_id,
            output_dir=pages_dir
        )
        if verbose:
            print("\n[OK] Download complete")
        return 0
    except Exception as e:
        print(f"[FAIL] Download failed: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Sync Canvas pages with local markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python canvas_sync.py up              Upload to default course
  python canvas_sync.py down --verbose  Download with progress info
  python canvas_sync.py up --course 123 Upload to specific course
        """
    )

    parser.add_argument(
        'command',
        choices=['up', 'down'],
        help='Sync direction: up (upload) or down (download)'
    )

    parser.add_argument(
        '--course',
        type=int,
        default=DEFAULT_COURSE_ID,
        help=f'Canvas course ID (default: {DEFAULT_COURSE_ID})'
    )

    parser.add_argument(
        '--pages-dir',
        default=DEFAULT_PAGES_DIR,
        help=f'Directory for Canvas pages (default: {DEFAULT_PAGES_DIR})'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress information'
    )

    args = parser.parse_args()

    # Load Canvas API token from .env (located one level up from code directory)
    if args.verbose:
        print("Loading Canvas API credentials...\n")

    # Get the path to the .env file (parent of code directory)
    script_dir = Path(__file__).parent
    env_path = script_dir.parent / '.env'

    canvastask.load_env(str(env_path))

    # Check if token exists
    if not os.environ.get('CANVAS_TOKEN'):
        print("[FAIL] Error: CANVAS_TOKEN not found in .env file", file=sys.stderr)
        print(f"Please ensure .env exists at: {env_path}", file=sys.stderr)
        print("Format: CANVAS_TOKEN=your_token_here", file=sys.stderr)
        return 1

    # Execute command
    if args.command == 'up':
        return sync_up(args.course, args.pages_dir, args.verbose)
    elif args.command == 'down':
        return sync_down(args.course, args.pages_dir, args.verbose)


if __name__ == '__main__':
    sys.exit(main())
