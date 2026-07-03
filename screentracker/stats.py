import sqlite3

PRODUCTIVE_APPS = [

    "chatgpt",
    "github",
    "stackoverflow",
    "documentation",
    "docs",
    "visual studio code",
    "pycharm",
    "cursor",
    "jupyter",
    "notebook",
    "leetcode",
    "hackerrank",
    "research",
    "python",
    "mysql",
    "docker",
    "terminal",
    "claude",
    "linkedIn",
    "ubuntu",
    "docker",
    "vscode",
    "anti-gravity",
    "overleaf"
]

CODING_KEYWORDS = [

    "visual studio code",
    "vscode",
    "cursor",
    "pycharm",
    "python",
    "jupyter",
    "docker",
    "terminal",
    "ubuntu",
    "mysql",
    "claude",
    "chatgpt",
    "github"
]

from .storage import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)


def format_time(seconds):

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    secs = seconds % 60 

    return (
        f"{hours:02}:"
        f"{minutes:02}:"
        f"{secs:02}"
    )


# ACTIVE TIME
def get_total_active_time():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    """)

    total = cursor.fetchone()[0] or 0

    conn.close()

    return total


# IDLE TIME
def get_total_idle_time():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(duration)
    FROM idle_usage
    WHERE DATE(start_time)=DATE('now')
    """)

    total = cursor.fetchone()[0] or 0

    conn.close()

    return total


# CODING TIME
def get_coding_time():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        app_name,
        window_title,
        duration
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    """)

    rows = cursor.fetchall()

    conn.close()

    coding_time = 0

    for app, title, duration in rows:

        text = f"{app} {title}".lower()

        if any(
            keyword in text
            for keyword in CODING_KEYWORDS
        ):

            coding_time += duration

    return coding_time

# PRODUCTIVITY SCORE
def get_productivity_score():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        app_name,
        window_title,
        duration
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    """)

    rows = cursor.fetchall()

    conn.close()

    productive = 0

    total = 0

    for app, title, duration in rows:

        total += duration

        text = f"{app} {title}".lower()

        if any(
            keyword in text
            for keyword in PRODUCTIVE_APPS
        ):

            productive += duration

    if total == 0:
        return 0

    return round(
        (productive / total) * 100,
        1
    )


# TOP APPS

def get_top_apps(limit=8):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        app_name,
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    GROUP BY app_name
    ORDER BY SUM(duration) DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# TOP ACTIVITIES

def get_top_activities(limit=8):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        window_title,
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    GROUP BY window_title
    ORDER BY SUM(duration) DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_hourly_usage():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        CAST(strftime('%H', start_time) AS INTEGER),
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    GROUP BY strftime('%H', start_time)
    """)

    rows = cursor.fetchall()

    conn.close()

    hourly = {
        hour: 0
        for hour in range(24)
    }

    for hour, duration in rows:

        hourly[hour] = duration

    return hourly