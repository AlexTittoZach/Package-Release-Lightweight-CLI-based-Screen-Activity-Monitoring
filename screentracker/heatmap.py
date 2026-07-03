import sqlite3

DB_NAME = "usage.db"


def get_hourly_usage():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        strftime('%H', start_time),
        SUM(duration)
    FROM app_usage
    WHERE DATE(start_time)=DATE('now')
    GROUP BY strftime('%H', start_time)
    ORDER BY strftime('%H', start_time)
    """)

    rows = cursor.fetchall()

    conn.close()

    hourly = {
        f"{i:02}": 0
        for i in range(24)
    }

    for hour, duration in rows:

        hourly[hour] = duration or 0

    return hourly


def format_duration(seconds):

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    secs = seconds % 60

    return (
        f"{hours:02}:"
        f"{minutes:02}:"
        f"{secs:02}"
    )


def generate_heatmap():

    hourly = get_hourly_usage()

    max_duration = max(
        hourly.values()
    )

    if max_duration == 0:
        max_duration = 1

    print("\nToday's Activity Heatmap\n")

    print(
        f"{'Hour':<8}"
        f"{'Heatmap':<45}"
        f"{'Time'}"
    )

    print("=" * 70)

    for hour, duration in hourly.items():

        bar_length = int(
            (
                duration / max_duration
            ) * 40
        )

        bar = "▓" * bar_length

        print(
            f"{hour}:00   "
            f"{bar:<40} "
            f"{format_duration(duration)}"
        )


if __name__ == "__main__":

    generate_heatmap()