import os
import re
import glob
import pandas as pd
import difflib

def normalize_name(name):
    # Remove extra spaces, lowercase, remove punctuation
    if not isinstance(name, str):
        return ""
    name = re.sub(r'[^\w\s]', '', name.lower())
    return " ".join(name.split())

def match_student(target_name, roster_names_normalized):
    norm_target = normalize_name(target_name)
    if not norm_target:
        return None
    
    # Exact match
    if norm_target in roster_names_normalized:
        return roster_names_normalized[norm_target]
    
    # Try fuzzy matching
    matches = difflib.get_close_matches(norm_target, roster_names_normalized.keys(), n=1, cutoff=0.7)
    if matches:
        return roster_names_normalized[matches[0]]
        
    # Try word overlap (e.g. if one has a middle name and the other doesn't)
    target_words = set(norm_target.split())
    best_match = None
    best_overlap = 0
    for r_norm, original_name in roster_names_normalized.items():
        r_words = set(r_norm.split())
        overlap = len(target_words.intersection(r_words))
        # Need at least 2 words matching if possible, or 1 if it's a very unique word
        if overlap > best_overlap and overlap >= len(target_words) - 1:
            best_overlap = overlap
            best_match = original_name
            
    if best_match:
        return best_match
        
    return None

def main():
    roster_path = r'y:\Hunter\eco331\grades\S26\midterm\midterm26.xlsx'
    submits_dirs = [
        r'y:\Hunter\eco331\canvas\canvas_submits',
        r'y:\Hunter\eco331\canvas\canvas_submits\summary'
    ]
    
    print("Loading roster...")
    try:
        roster_df = pd.read_excel(roster_path)
    except Exception as e:
        print(f"Error loading roster: {e}")
        return

    # Keep a normalized mapping
    roster_names = roster_df['Name'].dropna().tolist()
    roster_names_normalized = {normalize_name(name): name for name in roster_names}
    
    # We will build a new dataframe that starts with Name and SID
    tracker_df = roster_df[['Name', 'SID']].copy()
    
    # Dictionary to hold parsed assignment data:
    # assignment_data[assignment_name] = { official_name: days_late }
    assignment_data = {}
    unmatched_students = set()

    # Regex patterns
    title_pattern = re.compile(r'^###\s+Submissions for:\s+(.+)$', re.IGNORECASE)
    student_pattern = re.compile(r'^##\s+([^<]+?)\s*$')
    metadata_pattern1 = re.compile(r'<!--.*days_late:\s*([0-9\.\-]+).*-->', re.IGNORECASE)
    metadata_pattern2 = re.compile(r'\*\*Submitted:\*\*', re.IGNORECASE)

    for directory in submits_dirs:
        md_files = glob.glob(os.path.join(directory, '*.md'))
        for file_path in md_files:
            # Skip readme or other non-submission files if needed
            if 'readme' in file_path.lower():
                continue
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Quick check if file contains '## ' which indicates student submissions
            if '\n## ' not in content and not content.startswith('## '):
                continue
                
            lines = content.split('\n')
            
            # Find assignment title
            assignment_title = os.path.basename(file_path).replace('.md', '')
            for line in lines[:20]:
                match = title_pattern.search(line)
                if match:
                    assignment_title = match.group(1).strip()
                    break
                    
            if assignment_title not in assignment_data:
                assignment_data[assignment_title] = {}
                
            current_student = None
            
            for line in lines:
                # Check for student name
                stu_match = student_pattern.search(line)
                if stu_match:
                    raw_name = stu_match.group(1).strip()
                    matched_name = match_student(raw_name, roster_names_normalized)
                    
                    if matched_name:
                        current_student = matched_name
                        # Default days_late to 0 if we found their name, meaning they submitted
                        if current_student not in assignment_data[assignment_title]:
                            assignment_data[assignment_title][current_student] = 0.0
                    else:
                        unmatched_students.add(raw_name)
                        current_student = None
                    continue
                
                # If we are under a valid student block, look for metadata
                if current_student:
                    m1 = metadata_pattern1.search(line)
                    if m1:
                        try:
                            assignment_data[assignment_title][current_student] = float(m1.group(1))
                        except ValueError:
                            pass
                    elif metadata_pattern2.search(line):
                        # We know they submitted, days_late info isn't here, default to 0.0
                        if current_student not in assignment_data[assignment_title]:
                            assignment_data[assignment_title][current_student] = 0.0

    print(f"\nFound {len(assignment_data)} assignments.")
    
    for assignment, student_lateness in assignment_data.items():
        completed_col = f"{assignment} - Completed"
        lateness_col = f"{assignment} - Days Late"
        
        tracker_df[completed_col] = tracker_df['Name'].apply(lambda x: x in student_lateness)
        tracker_df[lateness_col] = tracker_df['Name'].apply(lambda x: student_lateness.get(x, None))

    output_path = r'y:\Hunter\eco331\canvas\assignment_tracker.xlsx'
    tracker_df.to_excel(output_path, index=False)
    print(f"\nSuccessfully saved tracker to {output_path}")
    
    if unmatched_students:
        print("\nWARNING: The following student names from canvas could not be matched to the roster:")
        for name in sorted(unmatched_students):
            if name.lower() not in ['neolithic revolution: summary', 'summary', 'submission text']:
                print(f"  - {name}")

if __name__ == "__main__":
    main()
