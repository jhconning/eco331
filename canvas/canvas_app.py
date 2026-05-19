# streamlit run canvas/canvas_app.py


import streamlit as st
import pandas as pd
import os
import glob
from pathlib import Path
import time
from datetime import datetime

# Important: Must be the first Streamlit command
st.set_page_config(page_title="Canvas LMS Manager", page_icon="🎓", layout="wide")

import sys
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

try:
    import canvastask
    import grade_submissions
except ImportError as e:
    st.error(f"Error importing modules: {str(e)}")
    st.stop()

# --- Config & Initialization ---
DEFAULT_COURSE_ID = 14011875  # Eco 331 S26
SUBMITS_DIR = current_dir / "canvas_submits"
RUBRICS_DIR = SUBMITS_DIR / "rubrics"

# Ensure directories exist
os.makedirs(SUBMITS_DIR, exist_ok=True)
os.makedirs(RUBRICS_DIR, exist_ok=True)

def init_app():
    if 'connected' not in st.session_state:
        env_path = str(current_dir.parent / '.env')
        canvastask.load_env(env_path)
        
        token = os.environ.get('CANVAS_TOKEN')
        if token and token != 'your_token_here':
            user = canvastask.canvas_request('users/self')
            if user:
                st.session_state.connected = True
                st.session_state.user_name = user.get('name', 'Unknown User')
                st.toast(f"Connected to Canvas as {st.session_state.user_name}!", icon="✅")
            else:
                st.session_state.connected = False
        else:
             st.session_state.connected = False

init_app()

if not st.session_state.get('connected', False):
    st.error("❌ Failed to connect to Canvas. Please ensure your `.env` file contains a valid `CANVAS_TOKEN`.")
    st.stop()

# --- Sidebar Global Settings & Navigation ---
st.sidebar.title("🎓 Canvas Settings")
course_id = st.sidebar.number_input(
    "Course ID", 
    value=DEFAULT_COURSE_ID, 
    step=1,
    help="Find this in your Canvas Course URL"
)

st.sidebar.divider()

gemini_key = os.environ.get("GEMINI_API_KEY", "").strip('"').strip("'")
api_key = st.sidebar.text_input("Gemini API Key", value=gemini_key, type="password", help="Required for AI grading & summarization.")
if api_key:
    api_key = api_key.strip('"').strip("'")
    os.environ["GEMINI_API_KEY"] = api_key

st.sidebar.divider()
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select an action:", [
    "📥 1. Download Submissions",
    "🤖 2. AI Grade",
    "🔍 3. Review & Edit Grades",
    "📤 4. Upload to Canvas",
    "📝 Quiz Responses",
    "📄 Wiki Pages Sync"
])

# Fetching Data Functions (Cached)
@st.cache_data(ttl=300)
def get_assignments(course_id):
    # Fetch all pages of assignments to ensure none are missing
    app_token = os.environ.get('CANVAS_TOKEN')
    if not app_token:
        return []
    import requests
    url = f"{canvastask.CANVAS_BASE_URL}/courses/{course_id}/assignments"
    headers = {'Authorization': f'Bearer {app_token}'}
    params = {'per_page': 100}
    
    all_assignments = []
    
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            all_assignments.extend(response.json())
            # Canvas uses the 'Link' header for pagination.
            if 'next' in response.links:
                url = response.links['next']['url']
                params = None # params are already embedded in the next URL
            else:
                url = None
        else:
            print(f"Error fetching assignments: {response.text}")
            break
            
    return [a for a in all_assignments if a.get('published', False)]

@st.cache_data(ttl=300)
def get_quizzes(course_id):
    quizzes = canvastask.canvas_request(f'courses/{course_id}/quizzes', params={'per_page': 100})
    return [q for q in quizzes if q.get('published', False)] if quizzes else []


# === PAGE ROUTING ===

st.title(page.split(". ")[-1] if ". " in page else page[2:])

# ---------------------------------------------------------
# 1. DOWNLOAD SUBMISSIONS
# ---------------------------------------------------------
if page == "📥 1. Download Submissions":
    st.write("Download assignment submissions from Canvas to a markdown file. This file will include late-day tracking for grading.")
    assignments = get_assignments(course_id)
    
    if not assignments:
        st.warning("No published assignments found.")
    else:
        assign_options = {f"{a['name']} ({a['id']})": a for a in assignments}
        selected_assign_name = st.selectbox("Select Assignment", options=list(assign_options.keys()))
        assign_id = assign_options[selected_assign_name]['id']
        due_at = assign_options[selected_assign_name].get('due_at')
        
        if due_at:
            from datetime import datetime
            due_str = datetime.fromisoformat(due_at.replace('Z', '+00:00')).strftime('%b %d, %Y %I:%M %p')
            st.info(f"📅 **Due Date:** {due_str}")
        else:
            st.info("📅 **Due Date:** Not set")
            
        if st.button("Download Submissions", type="primary"):
            with st.spinner("Downloading from Canvas..."):
                filepath = canvastask.download_assignment_submissions(course_id, assign_id, output_dir=str(SUBMITS_DIR))
                if filepath:
                    st.success(f"Saved to `{filepath}`")
                    st.toast("Download complete!", icon="✅")
                else:
                    st.error("Download failed.")
                    
        st.divider()
        st.subheader("Generate AI Summary")
        st.write("Optionally, summarize a downloaded markdown file to identify themes and highlights.")
        md_files = sorted(glob.glob(str(SUBMITS_DIR / "*.md")), reverse=True)
        if md_files:
            summary_file = st.selectbox("Select Markdown File", [Path(f).name for f in md_files])
            if st.button("Summarize"):
                if not api_key:
                    st.error("Gemini API Key missing.")
                else:
                    with st.spinner("Generating summary..."):
                        from google import genai
                        client = genai.Client(api_key=api_key)
                        
                        file_to_read = SUBMITS_DIR / summary_file
                        content = file_to_read.read_text(encoding='utf-8')
                        if len(content) > 250000:
                            content = content[:250000] + "\n\n[Truncated]"
                            
                        prompt = f"Summarize themes, provide 6-8 student highlights with names, and 3-4 discussion questions based on these submissions:\n\n{content}"
                        try:
                            resp = client.models.generate_content(model='gemini-3.1-flash-lite-preview', contents=prompt)
                            file_to_read.write_text(file_to_read.read_text(encoding='utf-8') + f"\n\n---\n\n# AI GENERATED SUMMARY\n\n{resp.text}", encoding='utf-8')
                            st.success("Summary generated and appended to file!")
                            with st.expander("View AI Summary", expanded=True):
                                st.markdown(resp.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

# ---------------------------------------------------------
# 2. AI GRADE
# ---------------------------------------------------------
elif page == "🤖 2. AI Grade":
    st.write("Run the Gemini API over downloaded submissions to assign grades based on a rubric.")
    if not api_key:
        st.warning("⚠️ Enter your Gemini API Key in the sidebar to use AI Grading.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Select Submissions")
        md_files = sorted(glob.glob(str(SUBMITS_DIR / "*.md")), reverse=True)
        # Exclude rubrics directory from markdown list
        md_files = [f for f in md_files if 'rubric' not in str(f)]
        
        if md_files:
            sub_file = st.selectbox("Submissions File", [Path(f).name for f in md_files])
            full_sub_path = SUBMITS_DIR / sub_file
            
            # Preview metadata from markdown
            content = full_sub_path.read_text(encoding='utf-8', errors='ignore')
            first_lines = content.split('\n')[:10]
            st.code('\n'.join(first_lines), language='markdown')
        else:
            st.info("No submission files found. Go to Step 1 to download some.")
            sub_file = None
            
    with col2:
        st.subheader("2. Select Rubric")
        rubrics = sorted(glob.glob(str(RUBRICS_DIR / "*.md")))
        
        # UI for creating a new rubric
        new_rubric_name = st.text_input("Or create new rubric (filename without .md):")
        if new_rubric_name:
            new_path = RUBRICS_DIR / f"{new_rubric_name}.md"
            if not new_path.exists():
                new_path.write_text("# New Rubric\n\nAdd your instructions here...", encoding='utf-8')
                st.rerun()
                
        if rubrics:
            rubric_options = [Path(r).name for r in rubrics]
            rubric_file = st.selectbox("Rubric File", rubric_options)
            full_rubric_path = RUBRICS_DIR / rubric_file
            
            # Inline rubric editor
            current_rubric_text = full_rubric_path.read_text(encoding='utf-8')
            edited_rubric = st.text_area("Edit Rubric (saved automatically before grading)", 
                                       value=current_rubric_text, 
                                       height=300)
            
            # Save if edited
            if edited_rubric != current_rubric_text:
                full_rubric_path.write_text(edited_rubric, encoding='utf-8')
        else:
            st.info("No rubrics found. Create one above.")
            rubric_file = None
            
    st.divider()
    
    if sub_file and rubric_file and api_key:
        if st.button("🚀 Run AI Grading", type="primary", use_container_width=True):
            submissions = grade_submissions.parse_submissions(full_sub_path)
            st.info(f"Found {len(submissions)} submissions to grade.")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            from google import genai
            client = genai.Client(api_key=api_key)
            
            for i, sub in enumerate(submissions):
                status_text.text(f"Grading {i+1}/{len(submissions)}: {sub['name']}")
                res = grade_submissions.grade_submission(client, edited_rubric, sub['name'], sub['content'], sub['days_late'], sub.get('user_id', ''))
                if res:
                    results.append(res)
                progress_bar.progress((i + 1) / len(submissions))
                time.sleep(0.5)
                
            status_text.text("Finished grading!")
            if results:
                out_csv = SUBMITS_DIR / f"grades_{sub_file.replace('.md', '.csv')}"
                grade_submissions.save_grades_csv(results, out_csv)
                st.success(f"Grading complete! Saved to {out_csv.name}")
                st.balloons()
            else:
                st.error("No grades were successfully generated.")


# ---------------------------------------------------------
# 3. REVIEW & EDIT GRADES
# ---------------------------------------------------------
elif page == "🔍 3. Review & Edit Grades":
    st.write("Review AI grades, manually adjust scores, and fix any errors before uploading.")
    
    csv_files = sorted(glob.glob(str(SUBMITS_DIR / "grades_*.csv")), reverse=True)
    if not csv_files:
        st.info("No grade CSV files found. Run AI Grading first.")
    else:
        selected_csv = st.selectbox("Select Grades File", [Path(f).name for f in csv_files])
        full_csv_path = SUBMITS_DIR / selected_csv
        
        df = pd.read_csv(full_csv_path)
        
        # Stats layout
        if 'final_score' in df.columns:
            st.subheader("Summary Statistics")
            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.metric("Total Graded", len(df))
            sc2.metric("Mean Score", f"{df['final_score'].mean():.1f}")
            sc3.metric("Median Score", df['final_score'].median())
            sc4.metric("Penalized (Late)", len(df[df['days_late'] > 0]))
            
            # Simple bar chart for distribution
            dist = df['final_score'].value_counts().sort_index()
            st.bar_chart(dist)
            
        st.write("### Edit Grades Table")
        st.caption("Changes are saved instantly when you click out of a cell.")
        
        # Use st.data_editor to allow inline editing
        edited_df = st.data_editor(
            df, 
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "name": st.column_config.TextColumn("Student Name", disabled=True),
                "final_score": st.column_config.NumberColumn("Final Score", format="%d"),
                "base_score": st.column_config.NumberColumn("Base Score", format="%d"),
                "late_penalty": st.column_config.NumberColumn("Late Penalty", format="%d", disabled=True),
                "days_late": st.column_config.NumberColumn("Days Late", format="%d", disabled=True),
            }
        )
        
        # Automatically save back to CSV if edited
        if not df.equals(edited_df):
            edited_df.to_csv(full_csv_path, index=False)
            st.toast("Modifications saved!", icon="💾")


# ---------------------------------------------------------
# 4. UPLOAD TO CANVAS
# ---------------------------------------------------------
elif page == "📤 4. Upload to Canvas":
    st.write("Push final grades and comments back directly to students in Canvas.")
    
    assignments = get_assignments(course_id)
    if not assignments:
        st.warning("No assignments found.")
    else:
        # We need an assignment ID to push logic to
        assign_options = {f"{a['name']} ({a['id']})": a for a in assignments}
        dest_assign_name = st.selectbox("Target Assignment in Canvas", options=list(assign_options.keys()))
        assign_id = assign_options[dest_assign_name]['id']
        
        csv_files = sorted(glob.glob(str(SUBMITS_DIR / "*.csv")), reverse=True)
        if not csv_files:
            st.info("No CSV files found.")
        else:
            selected_csv = st.selectbox("Grades File to Upload", [Path(f).name for f in csv_files])
            full_csv_path = SUBMITS_DIR / selected_csv
            
            df = pd.read_csv(full_csv_path)
            st.dataframe(df.head(3), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            # Default to columns we generate
            if "user_id" in df.columns:
                primary_idx = list(df.columns).index("user_id")
            elif "name" in df.columns:
                primary_idx = list(df.columns).index("name")
            else:
                primary_idx = 0
            user_col = col1.selectbox("Name/ID Column", df.columns, index=primary_idx)
            score_col = col2.selectbox("Score Column", df.columns, index=list(df.columns).index("final_score") if "final_score" in df.columns else 0)
            
            comment_opts = ["(None)"] + list(df.columns)
            idx = comment_opts.index("comment") if "comment" in comment_opts else 0
            comment_col = col3.selectbox("Comment Column", comment_opts, index=idx)
            
            st.warning("Note: `canvastask.py` matches by checking if the student Name/ID in the CSV matches the Canvas roster verbatim. Fuzzy matching logic may need to be handled carefully.")

            if st.button("🚀 Push Grades to Canvas", type="primary"):
                with st.spinner("Pushing to Canvas..."):
                    c_col = comment_col if comment_col != "(None)" else None
                    res = canvastask.upload_grades_from_file(
                        course_id, 
                        assign_id, 
                        str(full_csv_path), 
                        user_id_col=user_col, 
                        score_col=score_col, 
                        comment_col=c_col
                    )
                    if res:
                        st.success("Grades uploaded successfully!")
                    else:
                        st.error("Upload failed or had warnings. Check the terminal.")


# ---------------------------------------------------------
# QUIZ RESPONSES & WIKI PAGES
# ---------------------------------------------------------
elif page == "📝 Quiz Responses":
    st.header("Download Quiz Responses")
    quizzes = get_quizzes(course_id)
    if not quizzes:
        st.warning("No published quizzes found.")
    else:
        quiz_options = {f"{q['title']} ({q['id']})": q for q in quizzes}
        selected_quiz = st.selectbox("Select a Quiz", options=list(quiz_options.keys()))
        q_id = quiz_options[selected_quiz]['id']
        
        if st.button("Download All Quiz Responses to Markdown", type="primary"):
            with st.spinner("Fetching quizzes..."):
                filepath = canvastask.download_quiz_responses(course_id, q_id)
                if filepath:
                    st.success(f"Saved: `{filepath}`")

elif page == "📄 Wiki Pages Sync":
    st.header("Sync Canvas Wiki Pages")
    colA, colB = st.columns(2)
    with colA:
        if st.button("⬇️ Download ALL Pages (Canvas -> Local)"):
            with st.spinner("Downloading..."):
                canvastask.download_canvas_pages_to_markdown(course_id, output_dir='canvas_pages')
                st.success("Download complete!")

    with colB:
        if st.button("⬆️ Upload ALL Pages (Local -> Canvas)"):
            with st.spinner("Uploading `.md` files..."):
                canvastask.upload_all_markdown_files(course_id, canvas_folder='canvas_pages')
                st.success("Upload complete!")
