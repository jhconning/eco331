# Canvas App Sandbox

This directory contains standalone Python scripts and Jupyter notebooks for managing interactions with your Canvas LMS course via the Canvas API. 

## File Overview

*   **`canvastask.py`**: The core library and workhorse module. It handles authentication and all low-level API operations, including downloading assignments and quizzes, syncing wiki pages, and making raw HTTP requests using your token.
*   **`canvas_app.py`**: A Streamlit web application that provides a graphical user interface (GUI) over the functions available in `canvastask.py`. Uses Gemini AI to optionally summarize submissions.
*   **`canvas_sync.py`**: A command-line interface (CLI) tool designed specifically for synchronizing Canvas Wiki Pages locally as Markdown files and uploading changes back to Canvas.
*   **`canvas_task.ipynb` & `canvas_api.ipynb`**: Interactive Jupyter notebooks demonstrating how to fetch data, grade submissions, and organize class material directly via code. They provide step-by-step examples.
*   **`CANVAS_SYNC_README.md`**: Dedicated documentation for using the `canvas_sync.py` CLI tool.

## Downloaded Data Directories

*   **`canvas_pages/`**: Holds Markdown files downloaded from Canvas Wiki Pages, allowing for local editing and version control.
*   **`canvas_quizzes/`**: Holds Markdown summaries of student quiz responses.
*   **`canvas_submits/`**: Holds files and generated AI summaries for assignment submissions.

## Running the Streamlit App

The Streamlit app acts as an interactive control panel for managing Canvas tasks. To invoke the app locally from the command line:

1.  Make sure your `.env` file containing `CANVAS_TOKEN` is available in the parent directory (`eco331/.env`). The scripts are expected to read it from there.
2.  Also ensure `GEMINI_API_KEY` is present in the `.env` file (or can be passed to the app UI at runtime) if you plan on summarizing assignment submissions using AI.
3.  Open a terminal (e.g., Anaconda Prompt, PowerShell, or command prompt), navigate to the `canvas` directory, and run the following command:
    ```bash
    cd "c:\Users\jonat\My Drive\Hunter\eco331\canvas"
    streamlit run canvas_app.py
    ```
4.  The application will automatically boot up and open in your default web browser on a development server port (usually `localhost:8501`).
