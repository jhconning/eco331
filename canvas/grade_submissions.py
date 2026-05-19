"""
AI-assisted grading module for Canvas submissions.
Uses Gemini API to grade each student submission against a dynamic rubric.
"""

import os
import re
import csv
import json
import time
from pathlib import Path
from google import genai

MODEL = "gemini-3.1-flash-lite-preview"

def parse_submissions(filepath):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    # Split on '---' separators 
    blocks = re.split(r'\n---+\n', text)
    submissions = []
    for block in blocks:
        block = block.strip()
        name_match = re.match(r'^## (.+)', block)
        if not name_match:
            continue
        name = name_match.group(1).strip()
        days_late = 0
        user_id = ''
        
        late_match = re.search(r'days_late:\s*(\d+)', block)
        if late_match:
            days_late = int(late_match.group(1))
            
        uid_match = re.search(r'user_id:\s*(\d+)', block)
        if uid_match:
            user_id = uid_match.group(1)
            
        content_lines = block.split('\n', 1)
        content = content_lines[1].strip() if len(content_lines) > 1 else ''
        if content and len(content) > 50:
            submissions.append({"name": name, "user_id": user_id, "content": content, "days_late": days_late})
    return submissions

def grade_submission(client, rubric_text, name, content, days_late=0, user_id=""):
    tone_instructions = """
---
CRITICAL INSTRUCTIONS FOR THE 'comment' FIELD:
- Address the student directly (e.g., use "You", not "The student").
- Maintain a friendly but professional, collegiate-level grading tone.
- AVOID overly enthusiastic or sycophantic praise (e.g. NEVER say "You did a fantastic job!" or "Great work!").
- Instead, use understated, professional praise, such as "Nicely explained", "Good analysis", or for outstanding work, "Very good, thought-provoking".
- If the student wrote something unusually insightful, funny, or creative, explicitly acknowledge it.
- Keep the comment concise (2-3 sentences max) and completely avoid typical "AI-sounding" robotic phrasing.
---
"""
    prompt = rubric_text + tone_instructions + f"\n\n## Student: {name}\n\n{content[:5000]}"
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        raw = response.text.strip()
        raw = re.sub(r'^```json\s*', '', raw, flags=re.MULTILINE)
        raw = re.sub(r'^```\s*', '', raw, flags=re.MULTILINE)
        raw = raw.strip()
        json_match = re.search(r'\{[^{}]*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            result['name'] = name
            result['user_id'] = user_id
            result['days_late'] = days_late
            
            # Use bonus fields if present, otherwise default to 0
            bonus = (
                result.get('part1_bonus', 0) +
                result.get('mechanisms_bonus', 0) +
                result.get('course_material_bonus', 0) +
                result.get('ai_critique_bonus', 0)
            )
            base_score = 6 + bonus
            if days_late > 10:
                late_penalty = 2
            elif days_late > 5:
                late_penalty = 1
            else:
                late_penalty = 0
                
            final_score = max(4, base_score - late_penalty)
            result['base_score'] = base_score
            result['late_penalty'] = late_penalty
            result['final_score'] = final_score
            
            breakdown = f"Base Score: {base_score}/10\n"
            if late_penalty > 0:
                breakdown += f"Late Penalty: -{late_penalty}\n"
            breakdown += f"Final Score: {final_score}/10\n\n"
            
            ai_comment = result.get('comment', 'No feedback provided.')
            result['comment'] = breakdown + ai_comment
            
            return result
        else:
            return {"name": name, "error": "No JSON found in response", "raw": raw[:200]}
    except Exception as e:
        return {"name": name, "error": str(e)}

def batch_grade(submissions, rubric_text, api_key, progress_callback=None):
    client = genai.Client(api_key=api_key)
    results = []
    
    for i, sub in enumerate(submissions):
        if progress_callback:
            progress_callback(i, len(submissions), sub['name'])
            
        result = grade_submission(client, rubric_text, sub['name'], sub['content'], sub['days_late'], sub.get('user_id', ''))
        if result:
            results.append(result)
        time.sleep(0.1)  # Avoid rate limits
        
    return results

def save_grades_csv(results, output_path):
    # Determine all possible keys to avoid KeyError if response format varies mildly
    fieldnames = ['user_id', 'name', 'days_late', 'part1_bonus', 'mechanisms_bonus', 'course_material_bonus',
                 'ai_critique_bonus', 'base_score', 'late_penalty', 'final_score', 'comment', 'error']
                 
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    return output_path
