import re
import datetime
from pathlib import Path
from collections import defaultdict, Counter

def parse_deadlines(readme_path):
    """
    Parses the README file to extract deadlines for each Day assignment.
    Returns a dictionary mapping 'DayX' (int) to datetime object.
    """
    deadlines = {}
    current_day = None
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find sections like "## Day X" or "### Assignment (day X)"
    # and subsequent deadlines. 
    # Since the structure is loosely markdown, iterating lines might be safer 
    # to keep context of which "Day" we are in.
    
    lines = content.splitlines()
    day_pattern = re.compile(r'^##\s+Day\s+(\d+)', re.IGNORECASE)
    # Some days might be inside "### Assignment (day 1)" blocks if not top level
    assignment_pattern = re.compile(r'###\s+Assignment\s+\(day\s+(\d+)\)', re.IGNORECASE)
    
    deadline_pattern = re.compile(r'\*\s+Dead-line:\s+(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})', re.IGNORECASE)

    for line in lines:
        # Check for Day header
        m_day = day_pattern.search(line)
        if m_day:
            current_day = int(m_day.group(1))
            continue
            
        m_assign = assignment_pattern.search(line)
        if m_assign:
            current_day = int(m_assign.group(1))
            continue

        # Check for Deadline
        if current_day is not None:
            m_dead = deadline_pattern.search(line)
            if m_dead:
                date_str = m_dead.group(1)
                # Parse date format: 2025.11.01 22:00
                dt = datetime.datetime.strptime(date_str, "%Y.%m.%d %H:%M")
                deadlines[current_day] = dt
                # Reset current_day so we don't accidentally assign same deadline to multiple days 
                # unless a new header is found. 
                # (Actually, strict reset might differ from file structure, but let's assume one deadline per section)
                # We won't reset current_day immediately in case the deadline line is far down, 
                # but typically it's the specific assignment deadline.
                
    return deadlines

def extract_days(text):
    """
    Extracts list of day numbers from a subject string.
    Handles: "Day 1", "Day01", "Day 1 and 2", "Day 1, 2", "Day 03 and Day 04"
    """
    matches = set()
    # Normalize simply to lower for regex flags
    # Find all "Day <num>" starts
    # We iterate manually to handle "chained" days like "Day 1 and 2"
    
    # Strategy: Find "Day \d+" patterns. Check immediately after for " and \d+" or ", \d+".
    # Note: "Day 03 and Day 04" will be caught as two separate "Day \d+" hits.
    # "Day 05 and 06" -> "Day 05" hit, then we check after for "and 06".
    
    # We strip to avoid issues, though regex handles whitespace
    
    # Find iter helps us get positions
    for m in re.finditer(r'day\s*(\d+)', text, re.IGNORECASE):
        matches.add(int(m.group(1)))
        
        # Check trailing parts for " and <num>" or ", <num>"
        # We look strictly from where this match ended
        current_pos = m.end()
        rest = text[current_pos:]
        
        while True:
            # Pattern: separator + number. Separator is "and", "&", ","
            # We don't want to match " and Day 4" here because the outer loop will catch "Day 4"
            # So we purposefully look for cases implies continuation of the previous "Day" word
            # i.e. NO "Day" word in between.
            
            # Check if next meaningful token is "Day" -> if so, break, outer loop handles it
            if re.match(r'\s*(and|,|&)\s*day', rest, re.IGNORECASE):
                break
                
            sub_m = re.match(r'\s*(?:and|,|&)\s*(\d+)', rest, re.IGNORECASE)
            if sub_m:
                 matches.add(int(sub_m.group(1)))
                 rest = rest[sub_m.end():]
            else:
                break
                
    return sorted(list(matches))

def parse_submissions(subjects_path):
    """
    Parses subjects.txt to extract submissions.
    Returns:
    - submissions: list of dicts {student, day, timestamp, subject_line}
    - unique_students: set of student names
    - format_counts: Counter of subject line formats
    """
    submissions = []
    unique_students = set()
    format_counts = Counter()
    
    with open(subjects_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            
            subject_text = parts[2].strip()
            timestamp_str = parts[-1].strip() if len(parts) >= 1 else None
            
            # Timestamp Parsing Fallback
            if timestamp_str and not re.match(r'\d{4}-\d{2}-\d{2}T', timestamp_str):
                 for p in reversed(parts):
                     if re.match(r'\d{4}-\d{2}-\d{2}T', p):
                         timestamp_str = p
                         break

            if not timestamp_str:
                continue

            try:
                ts = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                continue

def parse_submissions(subjects_path):
    """
    Parses subjects.txt to extract submissions.
    Returns:
    - submissions: list of dicts {student, day, timestamp, subject_line}
    - unique_students: set of student names
    - format_counts: Counter of subject line formats
    """
    submissions = []
    unique_students = set()
    format_counts = Counter()
    
    with open(subjects_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            
            subject_text = parts[2].strip()
            timestamp_str = parts[-1].strip() if len(parts) >= 1 else None
            
            # Timestamp Parsing Fallback
            if timestamp_str and not re.match(r'\d{4}-\d{2}-\d{2}T', timestamp_str):
                 for p in reversed(parts):
                     if re.match(r'\d{4}-\d{2}-\d{2}T', p):
                         timestamp_str = p
                         break

            if not timestamp_str:
                continue

            try:
                ts = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                continue

def parse_submissions(subjects_path):
    """
    Parses subjects.txt to extract submissions.
    Returns:
    - submissions: list of dicts {student, day, timestamp, subject_line}
    - unique_students: set of student names
    - format_counts: Counter of subject line formats
    """
    submissions = []
    unique_students = set()
    format_counts = Counter()
    
    with open(subjects_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            
            subject_text = parts[2].strip()
            timestamp_str = parts[-1].strip() if len(parts) >= 1 else None
            
            # Timestamp Parsing Fallback
            if timestamp_str and not re.match(r'\d{4}-\d{2}-\d{2}T', timestamp_str):
                 for p in reversed(parts):
                     if re.match(r'\d{4}-\d{2}-\d{2}T', p):
                         timestamp_str = p
                         break

            if not timestamp_str:
                continue

            try:
                ts = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                continue

            # Analyze Format Stats
            if " by " in subject_text.lower():
                format_counts["Day XX by Name"] += 1
            elif "-" in subject_text:
                format_counts["Day XX - Name"] += 1
            else:
                format_counts["Other"] += 1

            # Extract Days first
            days = extract_days(subject_text)
            
            if days:
                # Attempt to split name from format
                # 1. Try " by "
                split_by = re.split(r'\s+by\s+', subject_text, maxsplit=1, flags=re.IGNORECASE)
                if len(split_by) == 2:
                    current_name = split_by[1]
                else:
                    # 2. Try " - "
                    split_dash = re.split(r'\s+-\s+', subject_text, maxsplit=1)
                    if len(split_dash) == 2:
                        current_name = split_dash[1]
                    else:
                        # 3. Fallback: Use the whole text
                        current_name = subject_text

                # Now clean `current_name`
                
                # Remove "Day \d+" (in case fallback used)
                cleaned_name = re.sub(r'day\s*\d+', '', current_name, flags=re.IGNORECASE)
                
                # Remove "Proposal for..." junk (case insensitive)
                # Matches: "Proposal for final project", "Final project proposal", "Project proposal"
                cleaned_name = re.sub(r'(proposal\s+for\s+(final\s+)?project)|((final\s+)?project\s+proposal\s*(for)?)', '', cleaned_name, flags=re.IGNORECASE)
                
                # Remove "and \d+" or ", \d+" (chained days artifacts)
                cleaned_name = re.sub(r'(?:and|&|,)\s*\d+', '', cleaned_name, flags=re.IGNORECASE)
                
                # Remove "by" artifact (if fallback used)
                cleaned_name = re.sub(r'\bby\b', '', cleaned_name, flags=re.IGNORECASE)
                
                # Remove leading "And" / "For" / separators
                # e.g. "And Einav Litvak" -> "Einav Litvak"
                cleaned_name = re.sub(r'^\s*(and|&|for)\s+', '', cleaned_name, flags=re.IGNORECASE)
                
                # Remove separators from edges
                cleaned_name = re.sub(r'^[\s\-:]+|[\s\-:]+$', '', cleaned_name)
                
                # Normalize hyphens to spaces to merge "Name-Surname" and "Name Surname"
                # User says "names do not repeat... assume same person"
                cleaned_name = cleaned_name.replace('-', ' ')
                
                # Compress spaces
                cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
                
                # Title Case
                name = cleaned_name.title()
                
                # Edge case: Empty name?
                if not name:
                    name = "Unknown"

                unique_students.add(name)
                for d in days:
                    submissions.append({
                        'student': name,
                        'day': d,
                        'timestamp': ts,
                        'original_line': subject_text
                    })
            else:
                pass

    # Deduplicate: Keep earliest submission for each (student, day)
    # Sort by timestamp first to ensure we process in chronological order
    submissions.sort(key=lambda x: x['timestamp'])
    
    unique_map = {} # (student, day) -> submission
    deduped_submissions = []
    
    for sub in submissions:
        key = (sub['student'], sub['day'])
        if key not in unique_map:
            unique_map[key] = sub
            deduped_submissions.append(sub)
    
    return deduped_submissions, unique_students, format_counts

def analyze_data(deadlines, submissions, all_students):
    """
    Analyzes the parsed data to generate report sections.
    """
    # 1. Missing Assignments
    # We assume assignments are Day 1 to Day 9
    # But let's detect the range from deadlines
    target_days = sorted(deadlines.keys())
    
    missing_assignments = defaultdict(list) # student -> list of missing days
    
    # Map student -> set of submitted days
    student_submissions = defaultdict(set)
    for sub in submissions:
        student_submissions[sub['student']].add(sub['day'])
        
    for student in sorted(all_students):
        for day in target_days:
            if day not in student_submissions[student]:
                missing_assignments[student].append(day)

    # 2. Late Submissions & 3. Time Distribution
    late_submissions = [] # list of (student, day, delta)
    time_deltas = [] # list of timedelta
    
    for sub in submissions:
        day = sub['day']
        if day in deadlines:
            deadline = deadlines[day]
            # Naive comparison (ensure both are aware or naive)
            # deadlines are parsed with strptime (naive)
            # submissions are parsed with strptime (naive)
            # But subjects.txt has 'Z', so we might need to handle timezone.
            # python's strptime %z works if Z is +0000, but often %Z or manual handling is needed for straight 'Z'.
            # My parser used "%Y-%m-%dT%H:%M:%SZ" which usually produces a naive object in older python or requires specific handling.
            # Let's check if the generic parser produced naive. 
            # If naive, we assume UTC essentially.
            
            # Actually, let's normalize to be safe.
            ts = sub['timestamp']
            
            # simple check
            delta = ts - deadline
            time_deltas.append(delta)
            
            if ts > deadline:
                late_submissions.append({
                    'student': sub['student'],
                    'day': day,
                    'delta': delta
                })

    return missing_assignments, late_submissions, time_deltas

import pandas as pd
import matplotlib.pyplot as plt


def calculate_stats(df, all_students, deadlines):
    """
    Calculates advanced statistics:
    - Completion Rate per Day
    - Student Consistency Score
    """
    if df.empty:
        return {}, {}
    
    # 1. Completion Rate per Day
    day_counts = df['day'].value_counts().sort_index()
    total_students = len(all_students)
    completion_rates = (day_counts / total_students * 100).to_dict()
    
    # 2. Student Consistency Score
    # Consistency = (On-time submissions / Total Deadlines passed) * 100
    # For simplicity, we compare against *all* deadlines (Day 1-9)
    # or just the deadlines that have passed? Let's assume all deadlines in README are targets.
    
    consistency_scores = {}
    target_days = sorted(deadlines.keys())
    
    for student in all_students:
        student_subs = df[df['student'] == student]
        on_time_count = 0
        for day in target_days:
            # Check if student submitted this day
            sub = student_subs[student_subs['day'] == day]
            if not sub.empty:
                # Check if on time
                # We need to re-check lateness here or assume 'delta' column exists if we add it to DF
                # Let's calculate delta relative to deadline
                ts = sub.iloc[0]['timestamp']
                deadline = deadlines[day]
                if ts <= deadline:
                    on_time_count += 1
        
        score = (on_time_count / len(target_days) * 100) if target_days else 0
        consistency_scores[student] = score
        
    return completion_rates, consistency_scores



# ==========================================
# FUTURE ENHANCEMENTS: EMAIL AUTOMATION
# ==========================================
class EmailNotifier:
    """
    Mock system to demonstrate how email notifications would work
    if 'subjects.txt' contained student email addresses.
    
    Hypothetical 'subjects.txt' format:
    Day 1 - Einav Litvak - einav@example.com - 2025-11-14T09:17:48
    """
    
    @staticmethod
    def send_email(to_email, subject, body):
        """
        Mock function to simulate sending an SMTP email.
        """
        print(f"[MOCK EMAIL] To: {to_email} | Subject: {subject}")
        print(f"Body: {body}\n")

    @staticmethod
    def notify_new_assignment(student_email, assignment_name, due_date):
        """
        Triggered when a new assignment is released.
        """
        subject = f"New Assignment Released: {assignment_name}"
        body = f"Hi! The assignment '{assignment_name}' is now available. Due date: {due_date}."
        EmailNotifier.send_email(student_email, subject, body)

    @staticmethod
    def notify_deadline_warning(student_email, assignment_name, hours_remaining):
        """
        Triggered 24 hours before deadline.
        """
        subject = f"Reminder: {assignment_name} Due Soon"
        body = f"You have {hours_remaining} hours left to submit {assignment_name}. Don't be late!"
        EmailNotifier.send_email(student_email, subject, body)

    @staticmethod
    def notify_overdue(student_email, assignment_name):
        """
        Triggered immediately after deadline passes if no submission found.
        """
        subject = f"OVERDUE: {assignment_name}"
        body = f"The deadline for {assignment_name} has passed and we haven't received your work."
        EmailNotifier.send_email(student_email, subject, body)

    @staticmethod
    def notify_graded(student_email, assignment_name, grader_name):
        """
        Triggered when a TA updates the status.
        """
        subject = f"Grade Posted: {assignment_name}"
        body = f"Your submission for {assignment_name} has been reviewed by {grader_name}."
        EmailNotifier.send_email(student_email, subject, body)

# In a real implementation, you would extract emails in `parse_submissions`:
# email = parts[3].strip() if len(parts) > 3 else "unknown@weizmann.ac.il"
# submission['email'] = email

# And then use it in the analysis loop:
# if calculated_delta > 0:
#     EmailNotifier.notify_overdue(sub['email'], f"Day {sub['day']}")


def generate_plots(df, all_students, deadlines, output_dir):
    """
    Generates and saves:
    1. Heatmap (Student vs Day)
    2. Lateness Boxplot
    3. Submission Counts Bar Chart
    """
    if df.empty:
        return

    # Prepare DataFrame for Heatmap
    # Rows: Students, Cols: Days
    # Values: 0=Missing, 1=Late, 2=OnTime
    
    target_days = sorted(deadlines.keys())
    
    # Pre-calculate lateness (delta) if not in DF
    # We'll build a clean specific DF for plotting
    plot_data = []
    
    # We need a robust list of ALL students x ALL days
    # Default to missing
    for student in all_students:
        for day in target_days:
            status = 0 # Missing
            delta_hours = None
            
            # Find submission
            # Assuming deduped, so max 1 per student/day
            sub = df[(df['student'] == student) & (df['day'] == day)]
            
            if not sub.empty:
                ts = sub.iloc[0]['timestamp']
                deadline = deadlines[day]
                delta = ts - deadline
                delta_hours = delta.total_seconds() / 3600
                
                if delta.total_seconds() > 0:
                    status = 1 # Late
                else:
                    status = 2 # On Time
            else:
                pass 

            plot_data.append({
                'Student': student,
                'Day': day,
                'Status': status,
                'LatenessHours': delta_hours
            })
            
    plot_df = pd.DataFrame(plot_data)
    
    # --- 1. Heatmap using Matplotlib directly ---
    pivot_status = plot_df.pivot(index='Student', columns='Day', values='Status')
    # Fill NaN with 0 if any (shouldn't be, but safe)
    pivot_status = pivot_status.fillna(0)
    
    plt.figure(figsize=(10, len(all_students) * 0.4 + 2))
    
    # Colors: 0=Red, 1=Yellow, 2=Green
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(['#ffcccc', '#fff5cc', '#ccffcc']) 
    
    # We need to ensure values are 0, 1, 2. missing data/NaN might mess this up, 
    # but we filled missing with 0 above.
    
    plt.imshow(pivot_status, cmap=cmap, aspect='auto')
    
    # Ticks
    plt.xticks(range(len(pivot_status.columns)), pivot_status.columns)
    plt.yticks(range(len(pivot_status.index)), pivot_status.index)
    
    plt.title("Green=On Time, Yellow=Late, Red=Missing")
    plt.tight_layout()
    plt.savefig(output_dir / 'heatmap.png')
    plt.close()
    
    # --- 2. Lateness Boxplot ---
    submitted_only = plot_df.dropna(subset=['LatenessHours'])
    
    plt.figure(figsize=(10, 6))
    submitted_only.boxplot(column='LatenessHours', by='Day', grid=True, showfliers=False)
    # The 'boxplot' method creates a title automatically "Boxplot grouped by Day", remove it
    plt.suptitle('') 
    plt.title("Distribution of Lateness (Hours)")
    plt.axhline(0, color='red', linestyle='--', label="Deadline")
    plt.ylabel("Hours (Neg=Early, Pos=Late)")
    plt.savefig(output_dir / 'lateness_boxplot.png')
    plt.close()
    
    # --- 3. Submission Counts Bar Chart ---
    plt.figure(figsize=(10, 6))
    counts = plot_df[plot_df['Status'] > 0]['Day'].value_counts().sort_index()
    
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Total Submissions per Assignment")
    plt.xlabel("Day")
    plt.ylabel("Count")
    
    # Add labels
    for i, v in enumerate(counts.values):
        plt.text(i, v + 0.5, str(v), ha='center')
        
    plt.tight_layout()
    plt.savefig(output_dir / 'submission_counts.png')
    plt.close()

def generate_behavioral_plots(df, deadlines, output_dir):
    """
    Generates:
    1. Hourly Distribution (Histogram)
    2. Day of Week Distribution (Bar Chart)
    3. Procrastination Curve (Cumulative Line Chart)
    """
    if df.empty:
        return

    # --- 1. Hourly Distribution ---
    plt.figure(figsize=(10, 6))
    hours = df['timestamp'].dt.hour
    
    # Histogram bins 0-23
    plt.hist(hours, bins=range(25), edgecolor='black', color='teal', alpha=0.7, align='left')
    plt.title("Submission Time of Day (Hourly Distribution)")
    plt.xlabel("Hour of Day (0-23)")
    plt.ylabel("Frequency")
    plt.xticks(range(0, 24))
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_dir / 'hourly_distribution.png')
    plt.close()

    # --- 2. Day of Week Distribution ---
    plt.figure(figsize=(10, 6))
    # dt.day_name() gives Mon, Tue... but we want sorted order.
    # Let's assume standard Mon-Sun or Sun-Sat. Let's do Mon-Sun.
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = df['timestamp'].dt.day_name().value_counts().reindex(days_order).fillna(0)
    
    day_counts.plot(kind='bar', color='purple', edgecolor='black', rot=45)
    plt.title("Submissions by Day of Week")
    plt.xlabel("Day")
    plt.ylabel("Count")
    
    for i, v in enumerate(day_counts.values):
         plt.text(i, v + 0.5, str(int(v)), ha='center')
         
    plt.tight_layout()
    plt.savefig(output_dir / 'weekly_distribution.png')
    plt.close()

    # --- 3. Procrastination Curve (Cumulative) ---
    plt.figure(figsize=(10, 6))
    
    # Calculate delta for ALL submissions relative to their specific deadline
    deltas_hours = []
    
    for _, row in df.iterrows():
        day_num = row['day']
        if day_num in deadlines:
            deadline = deadlines[day_num]
            delta = row['timestamp'] - deadline
            deltas_hours.append(delta.total_seconds() / 3600)
            
    if deltas_hours:
        deltas_hours.sort()
        
        # We want to show the specific window around deadlines e.g. -7 days to +7 days
        # But let's plot all and maybe zoom or just plot simple CDF
        # Y axis: % of submissions
        # X axis: Time relative to deadline (Hours)
        
        y_vals = [i / len(deltas_hours) * 100 for i in range(1, len(deltas_hours) + 1)]
        
        plt.plot(deltas_hours, y_vals, marker='.', linestyle='-', color='crimson')
        plt.axvline(0, color='black', linestyle='--', label='Deadline')
        plt.axhline(50, color='gray', linestyle=':', alpha=0.5)
        plt.axhline(90, color='gray', linestyle=':', alpha=0.5)
        
        plt.title("Procrastination Curve (Cumulative Submissions)")
        plt.xlabel("Hours Relative to Deadline (Negative=Early, Positive=Late)")
        plt.ylabel("Cumulative % of Submissions")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Optional: Set X limit to focus on the "Action" (-48h to +48h?)
        # User didn't specify, but full range is usually -300 to +300 hours given previous stats
        # Let's keep auto scaling but maybe add a focused version? 
        # For now, full range is honest.
        
        plt.tight_layout()
        plt.savefig(output_dir / 'procrastination_curve.png')
        plt.close()


def print_report(missing, late, deltas, formats, deadlines, completion_rates, consistency_scores, output_file=None):
    def _print(s):
        print(s)
        if output_file:
            output_file.write(s + "\n")

    _print("="*60)
    _print("COURSE ANALYSIS REPORT")
    _print("="*60)
    
    _print("\n1. MISSING ASSIGNMENTS")
    _print("-" * 25)
    if not missing:
        _print("  None")
    for student, days in sorted(missing.items()):
        days_str = ", ".join(str(d) for d in days)
        _print(f"  {student}: Day(s) {days_str}")
        
    _print("\n2. LATE SUBMISSIONS")
    _print("-" * 25)
    if not late:
        _print("  None")
    
    # Group by student
    late_by_student = defaultdict(list)
    for item in late:
        late_by_student[item['student']].append(item)
    
    for student in sorted(late_by_student.keys()):
        _print(f"  {student}:")
        # Sort by day for cleaner output
        for item in sorted(late_by_student[student], key=lambda x: x['day']):
            _print(f"    Day {item['day']}: {item['delta']} late")
        
    _print("\n3. SUBMISSION TIME DISTRIBUTION")
    _print("(Relative to deadline: negative = early, positive = late)")
    _print("-" * 25)
    if deltas:
        early = [d for d in deltas if d.total_seconds() <= 0]
        late_deltas = [d for d in deltas if d.total_seconds() > 0]
        
        _print(f"  Total Submissions: {len(deltas)}")
        _print(f"  Early/On-time:     {len(early)}")
        _print(f"  Late:              {len(late_deltas)}")
        
        # Simple stats
        avg_delta = sum(deltas, datetime.timedelta(0)) / len(deltas)
        _print(f"  Average Delta:     {avg_delta}")
        
        min_delta = min(deltas)
        max_delta = max(deltas)
        _print(f"  Earliest:          {min_delta}")
        _print(f"  Latest:            {max_delta}")
    else:
        _print("  No data")

    _print("\n4. SUBJECT FORMAT POPULARITY")
    _print("-" * 25)
    total_formats = sum(formats.values())
    for fmt, count in formats.most_common():
        pct = (count / total_formats * 100) if total_formats else 0
        _print(f"  {fmt:<25} {count:>3} ({pct:.1f}%)")
        
    _print("\n5. COMPLETION RATES")
    _print("-" * 25)
    for day, rates in sorted(completion_rates.items()):
        _print(f"  Day {day}: {rates:.1f}%")

    _print("\n6. STUDENT CONSISTENCY SCORES")
    _print("(Percentage of on-time submissions)")
    _print("-" * 25)
    # Sort by score desc, then name
    sorted_scores = sorted(consistency_scores.items(), key=lambda x: (-x[1], x[0]))
    for student, score in sorted_scores:
        _print(f"  {student:<25}: {score:.1f}%")

def main():
    base_dir = Path(__file__).parent.parent
    readme_path = base_dir / 'Day9' / 'README_day9.md'
    subjects_path = base_dir / 'Day9' / 'subjects.txt'
    output_path = base_dir / 'Day9' / 'report.txt'
    output_dir = base_dir / 'Day9'
    
    deadlines = parse_deadlines(readme_path)
    submissions_list, unique_students_set, formats = parse_submissions(subjects_path)
    
    # Convert list to DataFrame
    df = pd.DataFrame(submissions_list)
    all_students_sorted = sorted(list(unique_students_set))
    
    missing, late, deltas = analyze_data(deadlines, submissions_list, unique_students_set)
    
    # Advanced Stats
    compl_rates, consistency = calculate_stats(df, all_students_sorted, deadlines)
    
    # Generate Plots
    generate_plots(df, all_students_sorted, deadlines, output_dir)
    generate_behavioral_plots(df, deadlines, output_dir)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        print_report(missing, late, deltas, formats, deadlines, compl_rates, consistency, output_file=f)
    
    print(f"\nReport saved to: {output_path}")
    print(f"Plots saved to: {output_dir}")

if __name__ == "__main__":
    main()
