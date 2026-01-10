# Day 9: Course Analysis Report

This project analyzes student submissions (`subjects.txt`) against assignment deadlines (`README_day9.md`) to generate a comprehensive performance report and visual analytics.

Found a mistake in subjects.txt: If I understood correctly, the timestamps in that file are actually the time when the issues were closed and not when they were created (opened, assignment submitted). So some of the statistics are not correct.

## Files
*   `assignment_report.py`: The main script.
*   `requirements.txt`: Python dependencies.
*   `subjects.txt`: Raw submission data (Input).
*   `README_day9.md`: Assignment specifications and deadlines (Input).

## Features

### 1. Data Parsing & Normalization
*   **Generalized Date Extraction**: Handles simple "Day 1" and combined formats if there is an 'and' in the string.
*   **Name Cleaning**: Standardizes student names by removing artifacts like "Proposal for...", "Day X", and prefixes like "And"/"For".
*   **Deduplication**: Ensures only the *earliest* submission counts if a student submitted multiple times for the same day.

### 2. Analysis
*   Identifies **Missing Assignments**.
*   Calculates **Late Submissions** (Time Delta vs. Deadline).
*   Computes **Student Consistency Scores** (% of on-time submissions).
*   Tracks **Completion Rates** per assignment.

### 3. Visualization
Generates the following plots:
*   `heatmap.png`: A comprehensive grid of Student vs. Day status (Green=OnTime, Yellow=Late, Red=Missing).
*   `lateness_boxplot.png`: Distribution of lateness hours for each assignment.
*   `submission_counts.png`: Total number of submissions per day.
*   `hourly_distribution.png`: Histogram of submission times (Night Owls vs. Early Birds).
*   `weekly_distribution.png`: Submissions by Day of Week.
*   `procrastination_curve.png`: Cumulative submissions timeline relative to the deadline.

### 4. Future Enhancements (Email Automation)
If student email addresses were available, the system could be extended to support automated notifications:
*   **New Assignment**: Alert students when a new task is released.
*   **Deadline Warning**: Automated reminder 24 hours before the due date.
*   **Overdue Alert**: Notification immediately after the deadline passes.
*   **Grading Confirmation**: Notification when a submission has been reviewed by a TA or Professor.

## Usage
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the script:
    ```bash
    python assignment_report.py
    ```
3.  View the output report in `report.txt` and the generated PNG images in the folder.

## Use of AI
I used an AI assistant to help develop this script. Below are some prompts used:

*   **Regex Refinement**: "Modify the regex to handle combined subjects like 'Day 05 and 06' and split them into distinct entries."
*   **Name Normalization**: "Clean the student names by removing substrings like 'Proposal for Final Project' and handle cases like 'And Einav Litvak'."
*   **Visualization Ideas**: "What analysis and graphs can we generate to show student habits? Suggest ideas like 'Night Owls' or 'Procrastination Curves'."
*   **Pandas Integration**: "Refactor the standard list-based process to use a Pandas DataFrame for easier statistical analysis and plotting."
