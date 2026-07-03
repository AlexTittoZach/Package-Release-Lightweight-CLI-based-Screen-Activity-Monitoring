import sqlite3
import sys

PRODUCTIVE_APPS = [
    "Code.exe",
    "pycharm64.exe",
    "Cursor.exe",
    "WindowsTerminal.exe"
]

CODING_APPS = [
    "Code.exe",
    "pycharm64.exe",
    "Cursor.exe",
    "WindowsTerminal.exe"
]

DISTRACTING_KEYWORDS = [
    "YouTube",
    "Instagram",
    "Netflix",
    "Facebook",
    "Reels",
    "Shorts"
]


def format_time(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours}h {minutes}m {secs}s"


def get_connection():

    return sqlite3.connect("usage.db")


# ----------------------------------
# PRODUCTIVITY
# ----------------------------------

def productivity_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        app_name,
        window_title,
        duration
    FROM app_usage
    WHERE DATE(start_time) = DATE('now')
    """)

    rows = cursor.fetchall()

    productive_time = 0
    neutral_time = 0
    distracting_time = 0

    for app, title, duration in rows:

        if app in PRODUCTIVE_APPS:

            productive_time += duration

        elif any(
            keyword.lower() in title.lower()
            for keyword in DISTRACTING_KEYWORDS
        ):

            distracting_time += duration

        else:

            neutral_time += duration

    total_time = (
        productive_time
        + neutral_time
        + distracting_time
    )

    score = (
        (productive_time / total_time) * 100
        if total_time > 0 else 0
    )

    print("\nToday's Productivity")
    print("=" * 50)

    print(
        "Productive Time :",
        format_time(productive_time)
    )

    print(
        "Neutral Time    :",
        format_time(neutral_time)
    )

    print(
        "Distracting Time:",
        format_time(distracting_time)
    )

    print(
        f"\nProductivity Score: {score:.1f}%"
    )

    print("=" * 50)

    conn.close()


# ----------------------------------
# ACTIVITIES
# ----------------------------------

def activity_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        window_title,
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time) = DATE('now')
    GROUP BY window_title
    ORDER BY SUM(duration) DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    print("\nTop Activities Today")
    print("=" * 80)

    for title, duration in rows:

        print(
            f"{title[:55]:<55}"
            f"{format_time(duration)}"
        )

    print("=" * 80)

    conn.close()


# ----------------------------------
# CODING
# ----------------------------------

def coding_report():

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join(
        "?" for _ in CODING_APPS
    )

    query = f"""
    SELECT
        app_name,
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    AND app_name IN ({placeholders})
    GROUP BY app_name
    ORDER BY SUM(duration) DESC
    """

    cursor.execute(
        query,
        CODING_APPS
    )

    rows = cursor.fetchall()

    total = 0

    print("\nCoding Analytics")
    print("=" * 50)

    for app, duration in rows:

        total += duration

        print(
            f"{app:<20}"
            f"{format_time(duration)}"
        )

    print("=" * 50)

    print(
        "Total Coding Time:",
        format_time(total)
    )

    conn.close()


# ----------------------------------
# SUMMARY
# ----------------------------------

def summary_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    """)

    total_time = cursor.fetchone()[0] or 0

    cursor.execute("""
    SELECT
        app_name,
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    GROUP BY app_name
    ORDER BY SUM(duration) DESC
    LIMIT 1
    """)

    app_result = cursor.fetchone()

    cursor.execute("""
    SELECT
        window_title,
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    GROUP BY window_title
    ORDER BY SUM(duration) DESC
    LIMIT 1
    """)

    activity_result = cursor.fetchone()

    print("\nToday's Summary")
    print("=" * 50)

    print(
        "Total Active Time:",
        format_time(total_time)
    )

    if app_result:

        print(
            "Most Used App:",
            app_result[0],
            f"({format_time(app_result[1])})"
        )

    if activity_result:

        print(
            "Most Used Activity:",
            activity_result[0],
            f"({format_time(activity_result[1])})"
        )

    print("=" * 50)

    conn.close()


# ----------------------------------
# MAIN
# ----------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("""
Usage:

python analytics.py productivity
python analytics.py activities
python analytics.py coding
python analytics.py summary
        """)
        sys.exit()

    command = sys.argv[1].lower()

    if command == "productivity":

        productivity_report()

    elif command == "activities":

        activity_report()

    elif command == "coding":

        coding_report()

    elif command == "summary":

        summary_report()

    else:

        print("Unknown command")