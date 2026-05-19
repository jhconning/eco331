"""
Canvas LMS API Interface Module

Provides a Python interface to the Canvas LMS API for managing courses,
assignments, submissions, quizzes, and Canvas pages. Includes utilities for
synchronizing markdown content between local files and Canvas pages.

Functions:
    load_env() - Load environment variables from .env file
    canvas_request() - Make authenticated requests to Canvas API
    upload_markdown_to_canvas() - Convert markdown to HTML and upload as Canvas page
    download_canvas_pages_to_markdown() - Download Canvas pages as markdown files
    upload_all_markdown_files() - Batch upload markdown files to Canvas
    download_assignment_submissions() - Download all assignment submissions to markdown
    download_quiz_responses() - Download all quiz responses with questions and answers

Example:
    >>> import canvastask
    >>> canvastask.load_env()
    >>> courses = canvastask.canvas_request('courses', params={'enrollment_state': 'active'})
    >>> for course in courses:
    ...     print(course['name'])
"""

import os
import subprocess
import sys
from pathlib import Path

import requests
import markdown
import html2text
import frontmatter

# Configuration
CANVAS_BASE_URL = 'https://canvas.instructure.com/api/v1'


def load_env(filepath='../.env'):
    """
    Load environment variables from a .env file.

    Reads a .env file line by line and sets environment variables for each
    KEY=VALUE pair. Lines starting with '#' are treated as comments and ignored.

    Args:
        filepath (str): Path to the .env file. Default is '../.env'
                       (one level up from code directory)

    Returns:
        None

    Example:
        >>> load_env()
        Loaded .env file

        >>> load_env('custom/.env')
        Loaded .env file

    Notes:
        - If the file doesn't exist, prints a warning
        - Sets os.environ variables that can be accessed with os.environ.get()
        - Values containing '=' are split only on the first '='
    """
    env_path = Path(filepath)
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
        print('Loaded .env file')
    else:
        print(f'Warning: {filepath} not found')


def canvas_request(endpoint, method='GET', params=None, data=None):
    """
    Make an authenticated request to the Canvas API.

    Constructs a full Canvas API URL from the endpoint, adds authentication
    headers, and makes the HTTP request. Returns JSON response on success,
    prints error message on failure.

    Args:
        endpoint (str): Canvas API endpoint (e.g., 'users/self', 'courses',
                       'courses/{id}/assignments'). Do not include base URL.
        method (str): HTTP method. Options: 'GET' (default), 'POST', 'PUT', 'DELETE'
        params (dict, optional): Query parameters to append to URL. Default is None.
        data (dict, optional): JSON body data for POST/PUT requests. Default is None.

    Returns:
        dict or list or None: Parsed JSON response on success (usually a dict or list)
                             None on error

    Example:
        >>> user = canvas_request('users/self')
        >>> print(user['name'])

        >>> assignments = canvas_request('courses/123/assignments')
        >>> print(f"Found {len(assignments)} assignments")

        >>> canvas_request('courses/123/pages', method='PUT',
        ...               data={'wiki_page': {'title': 'New Page', 'body': '<p>Content</p>'}})

    Raises:
        EnvironmentError: If CANVAS_TOKEN is not set in environment

    Notes:
        - Requires CANVAS_TOKEN to be set in environment (via load_env())
        - On error, prints the status code and response text
        - All responses are assumed to be JSON format
    """
    canvas_token = os.environ.get('CANVAS_TOKEN')
    if not canvas_token:
        raise EnvironmentError('CANVAS_TOKEN not set. Call load_env() first.')

    url = f'{CANVAS_BASE_URL}/{endpoint}'
    headers = {
        'Authorization': f'Bearer {canvas_token}'
    }

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=data
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None


def upload_markdown_to_canvas(course_id, title, md_content, published=False):
    """
    Convert markdown to HTML and upload as a Canvas page.

    Converts markdown content (with support for tables, code blocks, TOC) to HTML
    and uploads it to Canvas as a wiki page. If the page already exists (same URL slug),
    it will be updated.

    Args:
        course_id (int): Canvas course ID
        title (str): Page title. Used both as display title and to generate URL slug.
                    Title "Course Notes" becomes URL slug "course-notes".
        md_content (str): Markdown content to upload
        published (bool): Whether to publish the page immediately. If False, page
                         will be saved as draft. Default is False.

    Returns:
        dict or None: Canvas page API response data on success (includes 'title'
                     and 'url' keys), None on error

    Example:
        >>> md = "# Lecture 1\n\nThis is the content"
        >>> result = upload_markdown_to_canvas(123, "Lecture 1", md, published=True)
        >>> if result:
        ...     print(f"Page URL: {result['url']}")

    Notes:
        - Page URL slug is derived from title by converting to lowercase and
          replacing spaces with hyphens
        - Uses markdown extensions: tables, fenced_code, toc
        - Prints success message with Canvas URL if upload succeeds
        - If update fails, prints error to console
    """
    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )

    # Create URL slug from title
    url_slug = title.lower().replace(' ', '-')
    url_slug = ''.join(c for c in url_slug if c.isalnum() or c == '-')

    # Try to update existing page or create new one
    result = canvas_request(
        f'courses/{course_id}/pages/{url_slug}',
        method='PUT',
        data={
            'wiki_page': {
                'title': title,
                'body': html_content,
                'published': published
            }
        }
    )

    if result:
        status = "published" if published else "draft"
        print(f"Page '{title}' uploaded successfully ({status})")
        print(f"URL: https://canvas.instructure.com/courses/{course_id}/pages/{url_slug}")

    return result


def download_canvas_pages_to_markdown(course_id, output_dir='canvas'):
    """
    Download all Canvas pages from a course as markdown files with YAML frontmatter.

    Fetches all wiki pages from a Canvas course, converts HTML content to markdown,
    and saves each page as a markdown file. YAML frontmatter is added to preserve
    the page title and publication status.

    Args:
        course_id (int): Canvas course ID
        output_dir (str): Directory to save markdown files. Created if it doesn't exist.
                         Default is 'canvas' (relative to current directory).

    Returns:
        None

    Example:
        >>> download_canvas_pages_to_markdown(123)
        Downloading 5 pages to /absolute/path/to/canvas

          [OK] Course Syllabus
             → course_syllabus.md (published)
          [OK] Week 1 Notes
             → week_1_notes.md (draft)

        Downloaded 5 pages to /absolute/path/to/canvas

    Side Effects:
        - Creates output_dir if it doesn't exist
        - Writes .md files to output_dir
        - Prints progress information to console

    Notes:
        - Skips pages with no content
        - Filenames are derived from page titles, converted to lowercase with
          underscores and with special characters removed
        - HTML to markdown conversion uses html2text library
        - YAML frontmatter includes 'title' (for reference) and 'published' (true/false)
        - Requires python-frontmatter package
    """
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Get list of pages with pagination
    pages_list = []
    page = 1
    while True:
        pages = canvas_request(f'courses/{course_id}/pages', params={'per_page': 100, 'page': page})
        if not pages or len(pages) == 0:
            break
        pages_list.extend(pages)
        page += 1

    if not pages_list:
        print("No pages found")
        return

    # Initialize HTML to markdown converter
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0  # Don't wrap lines

    print(f"Downloading {len(pages_list)} pages to {output_path}\n")

    downloaded = 0
    for page_summary in pages_list:
        title = page_summary.get('title', 'Untitled')
        page_url = page_summary.get('url', '')

        # Fetch the full page content
        page = canvas_request(f'courses/{course_id}/pages/{page_url}')

        if not page:
            print(f"  Error: Could not fetch {title}")
            continue

        html_body = page.get('body', '')

        if not html_body:
            print(f"  Skipped: {title} (no content)")
            continue

        # Convert HTML to markdown
        md_content = h.handle(html_body)

        # Create filename from title
        filename = title.lower().replace(' ', '_').replace(':', '').replace('?', '')
        filename = ''.join(c for c in filename if c.isalnum() or c in ('_', '-'))
        filename = f"{filename}.md"

        filepath = output_path / filename

        # Create YAML frontmatter
        post = frontmatter.Post(md_content)
        post.metadata['published'] = page.get('published', False)
        post.metadata['title'] = title

        # Write markdown file with frontmatter
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        status = "published" if page.get('published') else "draft"
        print(f"  [OK] {title}")
        print(f"     → {filename} ({status})")
        downloaded += 1

    print(f"\nDownloaded {downloaded} pages to {output_path}")


def upload_all_markdown_files(course_id, canvas_folder='canvas', default_published=False):
    """
    Batch upload all markdown files from a folder to Canvas pages.

    Reads all .md files from a folder and uploads each to Canvas as a page.
    Files can optionally include YAML frontmatter specifying publication status
    and custom title.

    Args:
        course_id (int): Canvas course ID
        canvas_folder (str): Directory containing markdown files. Default is 'canvas'
                            (relative to current directory).
        default_published (bool): Default publication status if not specified in
                                file frontmatter. Default is False (save as draft).

    Returns:
        None

    Example:
        >>> upload_all_markdown_files(123, canvas_folder='canvas')
        Uploading 3 markdown files to Canvas

        Page 'Course Outline' uploaded successfully (published)
        URL: https://canvas.instructure.com/courses/123/pages/course-outline
          [OK] published: course_outline.md

        Successfully uploaded 3/3 pages

    Side Effects:
        - Uploads pages to Canvas
        - Prints progress information to console

    YAML Frontmatter Format:
        Your markdown files can include YAML frontmatter like:
        ```
        ---
        published: true
        title: Custom Page Title
        ---

        # Page content here
        ```

    Notes:
        - If 'title' not specified in frontmatter, uses filename (with underscores
          converted to spaces and title-cased)
        - Files without frontmatter are treated as having no metadata
        - Prints summary of uploads at end
        - Requires python-frontmatter package
    """
    canvas_path = Path(canvas_folder)

    if not canvas_path.exists():
        print(f"Error: {canvas_folder} folder not found")
        return

    # Find all markdown files
    md_files = list(canvas_path.glob('*.md'))

    if not md_files:
        print(f"No markdown files found in {canvas_folder}")
        return

    print(f"Uploading {len(md_files)} markdown files to Canvas\n")

    uploaded = 0
    for md_file in md_files:
        # Parse the file with frontmatter
        post = frontmatter.load(str(md_file))

        # Extract metadata
        metadata = post.metadata
        md_content = post.content

        # Get title from frontmatter or filename
        title = metadata.get('title') or md_file.stem.replace('_', ' ').title()

        # Get published status from frontmatter or use default
        published = metadata.get('published', default_published)

        # Upload to Canvas
        result = upload_markdown_to_canvas(course_id, title, md_content, published=published)

        if result:
            status = "[OK] published" if published else "[OK] draft"
            print(f"  {status}: {md_file.name}")
            uploaded += 1
        else:
            print(f"  [FAIL] Failed to upload {md_file.name}\n")

    print(f"\nSuccessfully uploaded {uploaded}/{len(md_files)} pages")


def download_assignment_submissions(course_id, assignment_id, output_dir='canvas_submits'):
    """
    Download all submissions for an assignment to a markdown file.

    Auto-detects submission type (discussion topic, text entry, file upload, URL)
    and extracts content appropriately. Handles pagination to fetch all submissions.

    Args:
        course_id (int): Canvas course ID
        assignment_id (int): Canvas assignment ID
        output_dir (str): Directory to save markdown file. Default is 'canvas_submits'
                         (created if it doesn't exist).

    Returns:
        Path or None: Path to saved markdown file on success, None on error

    Example:
        >>> filepath = download_assignment_submissions(14011875, 61516327)
        >>> print(f"Saved to: {filepath}")

        Fetching submissions for: Introduce Yourself
          Fetched page 1 (54 submissions)

        [OK] Found 54 total submissions
        [OK] Saved 37 submissions to: canvas_submits/submissions_61516327_20260202_221918.md
          (17 students did not submit)

    Submission Types Handled:
        - discussion_topic: Extracts from discussion_entries with HTML→markdown conversion
        - online_text_entry: Extracts from body field
        - online_upload: Lists file attachments
        - online_url: Extracts and formats URL link

    Side Effects:
        - Creates output_dir if it doesn't exist
        - Writes .md file with timestamp
        - Prints progress to console

    Notes:
        - Automatically requests discussion_entries in API params
        - Uses html2text for better HTML→markdown conversion
        - Preserves formatting (bold, italics, links, lists)
        - Skips unsubmitted students
        - Includes instructor comments if present
    """
    from datetime import datetime

    # Initialize HTML to markdown converter
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines

    # Get assignment details to determine type
    assignment = canvas_request(f'courses/{course_id}/assignments/{assignment_id}')
    assignment_name = assignment.get('name', 'Assignment') if assignment else 'Assignment'
    assignment_type = assignment.get('submission_types', [None])[0] if assignment else None

    # Fetch all submissions with pagination
    all_submissions = []
    page = 1

    print(f"Fetching submissions for: {assignment_name}")

    while True:
        submissions = canvas_request(
            f'courses/{course_id}/assignments/{assignment_id}/submissions',
            params={
                'include[]': ['user', 'submission_comments', 'submission_history', 'discussion_entries'],
                'per_page': 100,
                'page': page
            }
        )

        if not submissions or len(submissions) == 0:
            break

        all_submissions.extend(submissions)
        print(f"  Fetched page {page} ({len(submissions)} submissions)")
        page += 1

    print(f"\n[OK] Found {len(all_submissions)} total submissions\n")

    # Get due date from assignment
    due_at_str = assignment.get('due_at') if assignment else None

    # Create markdown content header
    md_content = f"### Submissions for: {assignment_name}  \n"
    md_content += f"**Assignment ID:** {assignment_id}  \n"
    md_content += f"**Course ID:** {course_id}  \n"
    if assignment_type:
        md_content += f"**Submission Type:** {assignment_type}  \n"
    md_content += f"**Total Submissions:** {len(all_submissions)}  \n"
    if due_at_str:
        md_content += f"**Due:** {due_at_str}  \n"
    md_content += f"**Downloaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n"

    # Extract and add assignment description
    description_html = assignment.get('description', '') if assignment else ''
    if description_html:
        description_md = h.handle(description_html).strip()
        if description_md:
            md_content += f"#### Assignment Description\n"
            md_content += f"{description_md}\n\n"

    md_content += "---\n\n"

    # Parse due date once for late calculations
    due_date = None
    if due_at_str:
        from datetime import timezone
        try:
            due_date = datetime.fromisoformat(due_at_str.replace('Z', '+00:00'))
        except Exception:
            due_date = None

    # Process each submission
    submitted_count = 0

    for sub in all_submissions:
        user_name = sub.get('user', {}).get('name', 'Unknown')
        submitted_at = sub.get('submitted_at')
        submission_type = sub.get('submission_type')

        # Skip unsubmitted
        if not submitted_at:
            continue

        submitted_count += 1

        # Compute days late
        days_late = 0
        if due_date and submitted_at:
            try:
                submitted_date = datetime.fromisoformat(submitted_at.replace('Z', '+00:00'))
                delta = submitted_date - due_date
                days_late = max(0, delta.days)
            except Exception:
                days_late = 0

        body = ''

        # Extract content based on submission type
        if submission_type == 'discussion_topic':
            # Get content from discussion entries
            discussion_entries = sub.get('discussion_entries', [])
            if discussion_entries:
                message_html = discussion_entries[0].get('message', '')
                if message_html:
                    body = h.handle(message_html).strip()

        elif submission_type == 'online_text_entry':
            # Get from body field
            body_html = sub.get('body', '')
            if body_html:
                body = h.handle(body_html).strip()

            # Fallback to submission history
            if not body:
                history = sub.get('submission_history', [])
                if history:
                    latest = history[-1]
                    body_html = latest.get('body', '')
                    if body_html:
                        body = h.handle(body_html).strip()

        elif submission_type == 'online_upload':
            # List attachments
            attachments = sub.get('attachments', [])
            if attachments:
                body = "**Files:**\n"
                for att in attachments:
                    filename = att.get('filename', 'unknown')
                    size = att.get('size', 0)
                    size_kb = size / 1024 if size else 0
                    body += f"- {filename} ({size_kb:.1f} KB)\n"

        elif submission_type == 'online_url':
            # Extract URL
            url = sub.get('url', '')
            if url:
                body = f"[{url}]({url})"

        # If still no content, mark as empty
        if not body:
            body = "*No submission content*"

        # Add student section with metadata line for grader
        user_id = sub.get('user_id', '')
        md_content += f"## {user_name}\n"
        md_content += f"<!-- user_id: {user_id} | submitted_at: {submitted_at} | days_late: {days_late} -->\n\n"
        md_content += f"{body}\n\n"

        # Add submission comments if any
        comments = sub.get('submission_comments', [])
        if comments:
            md_content += f"### Comments ({len(comments)})\n\n"
            for comment in comments:
                author = comment.get('author_name', 'Unknown')
                comment_text = comment.get('comment', '')
                created = comment.get('created_at', '')

                # Convert comment HTML to markdown if needed
                if '<' in comment_text:
                    comment_text = h.handle(comment_text).strip()

                md_content += f"**{author}** ({created}):\n> {comment_text}\n\n"

        md_content += "---\n\n"

    # Save to file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"submissions_{assignment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = output_path / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"[OK] Saved {submitted_count} submissions to: {filepath.absolute()}")
    print(f"  ({len(all_submissions) - submitted_count} students did not submit)")

    return filepath


def download_quiz_responses(course_id, quiz_id, output_dir='canvas_quizzes'):
    """
    Download all student responses for a Canvas quiz and save as markdown.

    Fetches quiz questions, all student submissions, and their answers. Handles
    different question types (multiple choice, essay, true/false, etc.) and
    formats everything as readable markdown.

    Args:
        course_id (int): Canvas course ID
        quiz_id (int): Canvas quiz ID
        output_dir (str): Directory to save markdown file. Default is 'canvas_quizzes'
                         (created if it doesn't exist).

    Returns:
        Path or None: Path to saved markdown file on success, None on error

    Example:
        >>> filepath = download_quiz_responses(14011875, 12345)
        >>> print(f"Saved to: {filepath}")

        Fetching responses for quiz: Midterm Exam
          Fetched page 1 (25 submissions)

        [OK] Found 25 total submissions

          Fetching answers for 25 submissions...

        [OK] Saved 23 responses to: canvas_quizzes/quiz_responses_12345_20260209_143022.md
          (2 students did not complete the quiz)

    Question Types Handled:
        - multiple_choice_question: Shows selected option
        - true_false_question: Shows True/False
        - essay_question: Shows full text response
        - short_answer_question: Shows text response
        - multiple_answers_question: Shows all selected options
        - matching_question: Shows matched pairs
        - numerical_question: Shows numeric answer
        - fill_in_multiple_blanks_question: Shows filled blanks
        - multiple_dropdowns_question: Shows dropdown selections

    Side Effects:
        - Creates output_dir if it doesn't exist
        - Writes .md file with timestamp
        - Prints progress to console

    Notes:
        - Requires 3 API calls: quiz metadata, quiz questions, and submissions
        - Then fetches individual submission answers (one call per student)
        - HTML in questions/answers is converted to markdown
        - Skips students who didn't submit or finish the quiz
    """
    from datetime import datetime

    # Initialize HTML to markdown converter
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines

    # Step 1: Fetch quiz metadata
    quiz = canvas_request(f'courses/{course_id}/quizzes/{quiz_id}')
    if not quiz:
        print(f"[FAIL] Failed to fetch quiz {quiz_id}")
        return None

    quiz_title = quiz.get('title', 'Quiz')
    points_possible = quiz.get('points_possible', 0)
    question_count = quiz.get('question_count', 0)

    print(f"Fetching responses for quiz: {quiz_title}")

    # Step 2: Fetch quiz questions (with pagination)
    all_questions = []
    page = 1

    while True:
        questions = canvas_request(
            f'courses/{course_id}/quizzes/{quiz_id}/questions',
            params={'per_page': 100, 'page': page}
        )

        if not questions or len(questions) == 0:
            break

        all_questions.extend(questions)
        page += 1

    # Build questions lookup dict
    questions_by_id = {q['id']: q for q in all_questions}

    # Step 3: Fetch all quiz submissions (with pagination)
    all_submissions = []
    page = 1

    while True:
        submissions = canvas_request(
            f'courses/{course_id}/quizzes/{quiz_id}/submissions',
            params={
                'include[]': ['user'],
                'per_page': 100,
                'page': page
            }
        )

        if not submissions:
            break

        # Filter out submissions array - Canvas returns {'quiz_submissions': [...]}
        if isinstance(submissions, dict) and 'quiz_submissions' in submissions:
            submissions = submissions['quiz_submissions']

        # Check if we got any submissions after extraction
        if len(submissions) == 0:
            break

        all_submissions.extend(submissions)
        print(f"  Fetched page {page} ({len(submissions)} submissions)")
        page += 1

    print(f"\n[OK] Found {len(all_submissions)} total submissions\n")

    # Step 4: Fetch answers for each submission
    print(f"  Fetching answers for {len(all_submissions)} submissions...")

    completed_count = 0
    submission_data = []

    for idx, submission in enumerate(all_submissions, 1):
        submission_id = submission.get('id')
        workflow_state = submission.get('workflow_state')

        # Skip if not complete
        if workflow_state not in ['complete', 'pending_review']:
            continue

        # Fetch this submission's answers
        answers_response = canvas_request(f'quiz_submissions/{submission_id}/questions')

        if answers_response:
            # Canvas returns {'quiz_submission_questions': [...]}
            if isinstance(answers_response, dict) and 'quiz_submission_questions' in answers_response:
                answers = answers_response['quiz_submission_questions']
            else:
                answers = answers_response if isinstance(answers_response, list) else []

            submission['answers'] = answers
            submission_data.append(submission)
            completed_count += 1

    print(f"  [OK] Fetched answers for {completed_count} completed submissions\n")

    # Step 5: Generate markdown content
    md_content = f"### Quiz Responses for: {quiz_title}  \n"
    md_content += f"**Quiz ID:** {quiz_id}  \n"
    md_content += f"**Course ID:** {course_id}  \n"
    md_content += f"**Questions:** {question_count}  \n"
    md_content += f"**Points Possible:** {points_possible}  \n"
    md_content += f"**Total Submissions:** {len(all_submissions)}  \n"
    md_content += f"**Completed:** {completed_count}  \n"
    md_content += f"**Downloaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n"
    md_content += "---\n\n"

    # Process each completed submission
    for submission in submission_data:
        # Get user info
        user_id = submission.get('user_id')
        # Find user info from original submission list
        user_name = "Unknown"
        for sub in all_submissions:
            if sub.get('user_id') == user_id and 'user' in sub:
                user_name = sub['user'].get('name', 'Unknown')
                break

        score = submission.get('score', 0)
        started_at = submission.get('started_at', '')
        finished_at = submission.get('finished_at', '')
        attempt = submission.get('attempt', 1)

        # Add student header
        md_content += f"## {user_name}\n\n"
        md_content += f"**Score:** {score} / {points_possible} points  \n"
        md_content += f"**Attempt:** {attempt}  \n"
        md_content += f"**Started:** {started_at}  \n"
        md_content += f"**Finished:** {finished_at}  \n\n"

        # Process each answer
        answers = submission.get('answers', [])

        for answer_data in answers:
            question_id = answer_data.get('id')
            question_info = questions_by_id.get(question_id, {})

            question_name = question_info.get('question_name', f'Question {question_id}')
            question_text = question_info.get('question_text', '')
            question_type = question_info.get('question_type', 'unknown')
            question_points = question_info.get('points_possible', 0)

            # Convert HTML question text to markdown
            if question_text and '<' in question_text:
                question_text = h.handle(question_text).strip()

            md_content += f"### {question_name}\n"
            if question_text:
                md_content += f"{question_text}\n\n"
            md_content += f"**Type:** {question_type} | **Points:** {question_points}\n\n"

            # Format answer based on question type
            answer_text = _format_quiz_answer(
                answer_data,
                question_info,
                question_type,
                h
            )

            md_content += f"**Student Answer:**  \n{answer_text}\n\n"

        md_content += "---\n\n"

    # Step 6: Save to file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"quiz_responses_{quiz_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = output_path / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"[OK] Saved {completed_count} responses to: {filepath.absolute()}")
    if len(all_submissions) > completed_count:
        print(f"  ({len(all_submissions) - completed_count} students did not complete the quiz)")

    return filepath


def _format_quiz_answer(answer_data, question_info, question_type, html_converter):
    """
    Format a quiz answer based on question type.

    Args:
        answer_data (dict): Answer data from Canvas API
        question_info (dict): Question metadata
        question_type (str): Type of question
        html_converter (HTML2Text): HTML to markdown converter

    Returns:
        str: Formatted answer text
    """
    answer = answer_data.get('answer')

    # Essay or short answer (text response)
    if question_type in ['essay_question', 'short_answer_question']:
        if isinstance(answer, str):
            # Convert HTML to markdown if needed
            if '<' in answer:
                return html_converter.handle(answer).strip()
            return answer
        return str(answer) if answer else "*No answer provided*"

    # True/False
    elif question_type == 'true_false_question':
        return str(answer) if answer else "*No answer*"

    # Multiple choice (single answer)
    elif question_type == 'multiple_choice_question':
        if not answer:
            return "*No answer selected*"

        # Look up the answer text from question options
        answers_list = question_info.get('answers', [])
        for option in answers_list:
            if option.get('id') == answer:
                text = option.get('text', '')
                if text and '<' in text:
                    text = html_converter.handle(text).strip()
                return text or f"Option ID: {answer}"

        return f"Selected answer ID: {answer}"

    # Multiple answers (checkboxes)
    elif question_type == 'multiple_answers_question':
        if not answer or not isinstance(answer, list):
            return "*No answers selected*"

        answers_list = question_info.get('answers', [])
        selected_texts = []

        for ans_id in answer:
            for option in answers_list:
                if option.get('id') == ans_id:
                    text = option.get('text', '')
                    if text and '<' in text:
                        text = html_converter.handle(text).strip()
                    selected_texts.append(text or f"ID: {ans_id}")
                    break

        if selected_texts:
            return "- " + "\n- ".join(selected_texts)
        return "*No answers selected*"

    # Matching question
    elif question_type == 'matching_question':
        if not answer or not isinstance(answer, list):
            return "*No matches provided*"

        result = []
        for match in answer:
            if isinstance(match, dict):
                answer_id = match.get('answer_id')
                match_id = match.get('match_id')
                result.append(f"- Answer {answer_id} → Match {match_id}")

        return "\n".join(result) if result else "*No matches*"

    # Numerical or calculated
    elif question_type in ['numerical_question', 'calculated_question']:
        return str(answer) if answer is not None else "*No answer*"

    # Fill in multiple blanks
    elif question_type == 'fill_in_multiple_blanks_question':
        if isinstance(answer, dict):
            result = []
            for blank, value in answer.items():
                result.append(f"- {blank}: {value}")
            return "\n".join(result) if result else "*No answer*"
        return str(answer) if answer else "*No answer*"

    # Multiple dropdowns
    elif question_type == 'multiple_dropdowns_question':
        if isinstance(answer, dict):
            result = []
            for dropdown, value in answer.items():
                result.append(f"- {dropdown}: {value}")
            return "\n".join(result) if result else "*No answer*"
        return str(answer) if answer else "*No answer*"

    # File upload
    elif question_type == 'file_upload_question':
        # Note: File attachments may require separate handling
        return "*File upload (see Canvas for attachment)*"

    # Default fallback
    else:
        return str(answer) if answer else "*No answer provided*"

import csv
from pathlib import Path

def download_students(course_id, output_csv=None):
    """
    Download a list of active students in the course.
    
    Args:
        course_id (int): Canvas course ID
        output_csv (str, optional): Path to save the list as a CSV file.
                                   If provided, writes 'user_id' and 'name' columns.
                                   
    Returns:
        list: A list of dicts containing user 'id', 'name', 'sortable_name', and 'email'.
    """
    all_students = []
    page = 1
    
    print(f"Fetching students for course: {course_id}")
    
    while True:
        users = canvas_request(
            f'courses/{course_id}/users',
            params={
                'enrollment_type[]': ['student'],
                'enrollment_state[]': ['active'],
                'include[]': ['email'],
                'per_page': 100,
                'page': page
            }
        )
        
        if not users or len(users) == 0:
            break
            
        all_students.extend(users)
        print(f"  Fetched page {page} ({len(users)} students)")
        page += 1
        
    print(f"\n[OK] Found {len(all_students)} total active students\n")
    
    extracted_students = []
    for user in all_students:
        extracted_students.append({
            'user_id': user.get('id'),
            'name': user.get('name'),
            'sortable_name': user.get('sortable_name'),
            'email': user.get('login_id', user.get('email', ''))
        })
        
    if output_csv:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['user_id', 'name', 'sortable_name', 'email'])
            writer.writeheader()
            writer.writerows(extracted_students)
        print(f"[OK] Saved student list to: {output_path.absolute()}")
        
    return extracted_students


def download_assignment_grades(course_id, assignment_id, output_csv=None):
    """
    Download a list of student submissions for a specific assignment, including grades.
    
    Args:
        course_id (int): Canvas course ID
        assignment_id (int): Canvas assignment ID
        output_csv (str, optional): Path to save the list as a CSV file.
                                   If provided, writes a CSV with grade data.
                                   
    Returns:
        list: A list of dicts containing user grading info.
    """
    all_submissions = []
    page = 1
    
    print(f"Fetching grades for course {course_id}, assignment {assignment_id}")
    
    while True:
        submissions = canvas_request(
            f'courses/{course_id}/assignments/{assignment_id}/submissions',
            params={
                'include[]': ['user'],
                'per_page': 100,
                'page': page
            }
        )
        
        if not submissions or len(submissions) == 0:
            break
            
        all_submissions.extend(submissions)
        print(f"  Fetched page {page} ({len(submissions)} submissions)")
        page += 1
        
    print(f"\n[OK] Found {len(all_submissions)} total submissions\n")
    
    extracted_grades = []
    for sub in all_submissions:
        user = sub.get('user', {})
        extracted_grades.append({
            'user_id': sub.get('user_id'),
            'name': user.get('name'),
            'score': sub.get('score'),
            'workflow_state': sub.get('workflow_state'),
            'submitted_at': sub.get('submitted_at')
        })
        
    if output_csv:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['user_id', 'name', 'score', 'workflow_state', 'submitted_at'])
            writer.writeheader()
            writer.writerows(extracted_grades)
        print(f"[OK] Saved grades to: {output_path.absolute()}")
        
    return extracted_grades


def upload_grades_batch(course_id, assignment_id, grade_data):
    """
    Batch upload grades and comments for an assignment.
    
    Args:
        course_id (int): Canvas course ID
        assignment_id (int): Canvas assignment ID
        grade_data (dict): Dictionary mapping user_id to grading details.
                           Format: {user_id: {'score': 95, 'text_comment': 'Great job!'}}
                           
    Returns:
        dict: The Canvas progress API response for the background job.
    """
    payload = {'grade_data': {}}
    
    count = 0
    for user_id, details in grade_data.items():
        user_payload = {}
        if 'score' in details and details['score'] is not None:
            user_payload['posted_grade'] = details['score']
        if 'text_comment' in details and details['text_comment']:
            user_payload['text_comment'] = details['text_comment']
            
        if user_payload:
            payload['grade_data'][str(user_id)] = user_payload
            count += 1
            
    if count == 0:
        print("No valid scores provided in grade_data")
        return None
        
    print(f"Uploading grades for {count} students...")
    
    result = canvas_request(
        f'courses/{course_id}/assignments/{assignment_id}/submissions/update_grades',
        method='POST',
        data=payload
    )
    
    if result:
        print("[OK] Grade upload job successfully queued by Canvas!")
        if isinstance(result, dict):
            print(f"Job Status URL: {result.get('url')}")
    else:
        print("[FAIL] Failed to queue grade upload.")
        
    return result


def upload_grades_from_file(course_id, assignment_id, filepath, user_id_col='user_id', score_col='score', comment_col=None):
    """
    Read grades from a CSV or Excel file and upload them to Canvas in batches.
    
    Args:
        course_id (int): Canvas course ID
        assignment_id (int): Canvas assignment ID
        filepath (str): Path to local CSV or Excel file
        user_id_col (str): Column name containing the Canvas User ID
        score_col (str): Column name containing the grade/score
        comment_col (str, optional): Column name containing text comments
        
    Returns:
        dict: Result from upload_grades_batch
    """
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas is required for this function. `mamba install pandas`")
        return None
        
    filepath_obj = Path(filepath)
    if not filepath_obj.exists():
        print(f"Error: File not found: {filepath}")
        return None
        
    print(f"Reading grades from: {filepath_obj.name}")
    
    if filepath_obj.suffix.lower() == '.csv':
        df = pd.read_csv(filepath)
    elif filepath_obj.suffix.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(filepath)
    else:
        print(f"Error: Unsupported file type '{filepath_obj.suffix}'. Must be .csv or .xlsx")
        return None
        
    if user_id_col not in df.columns or score_col not in df.columns:
        print(f"Error: Could not find required columns '{user_id_col}' or '{score_col}' in file.")
        print(f"Available columns: {list(df.columns)}")
        return None
        
    grade_data = {}
    skipped = 0
    
    for _, row in df.iterrows():
        try:
            if pd.isna(row[user_id_col]) or pd.isna(row[score_col]):
                skipped += 1
                continue
                
            user_id = int(float(row[user_id_col]))
            score = row[score_col]
            
            details = {'score': score}
            
            if comment_col and comment_col in df.columns:
                comment = row[comment_col]
                if not pd.isna(comment):
                    details['text_comment'] = str(comment)
                    
            grade_data[user_id] = details
            
        except ValueError:
            skipped += 1
            
    if skipped > 0:
        print(f"Note: Skipped {skipped} rows due to invalid/missing data.")
        
    return upload_grades_batch(course_id, assignment_id, grade_data)
