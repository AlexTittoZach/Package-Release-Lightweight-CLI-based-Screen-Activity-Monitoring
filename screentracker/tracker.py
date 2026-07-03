import time
from datetime import datetime

from .single_instance_lock import (
    acquire_lock
)

from rich.live import Live
from rich.console import Group
from rich.table import Table

from .monitor import get_active_window
from .idle import get_idle_seconds

from .database import (
    init_db,
    save_usage,
    save_idle
)

from .runtime_state import current_state

from .stats import (
    get_total_active_time,
    get_total_idle_time,
    get_coding_time,
    get_productivity_score,
    get_top_apps,
    get_top_activities,
    get_hourly_usage,
    format_time
)


# CONFIG

IDLE_LIMIT = 30
SAVE_INTERVAL = 30

IGNORED_APPS = [
    "Unknown",
    "AsusKeyboardHost.exe"
]

IGNORED_TITLES = [
    "",
    "AsKeybdHkToast App Window"
]


# INIT VARIABLES

current_app = None
current_title = None

tracking_start = None


# SAVE SESSION

def save_current_session():

    global tracking_start

    if current_app is None:
        return

    end_time = datetime.now()

    duration = int(
        (
            end_time - tracking_start
        ).total_seconds()
    )

    if duration <= 0:
        return

    if (
        current_app not in IGNORED_APPS
        and current_title not in IGNORED_TITLES
    ):

        save_usage(
            current_app,
            current_title,
            str(tracking_start),
            str(end_time),
            duration
        )


# HEATMAP

def build_heatmap():

    table = Table(
        title="LIVE HEATMAP"
    )

    table.add_column(
        "Hour",
        width=8
    )

    table.add_column(
        "Heatmap",
        width=45
    )

    table.add_column(
        "Time",
        justify="right",
        width=10
    )

    hourly = get_hourly_usage()

    max_usage = max(
        hourly.values()
    )

    if max_usage == 0:
        max_usage = 1

    for hour in range(24):

        usage = hourly[hour]

        bar_length = int(
            (
                usage / max_usage
            ) * 37
        )

        bar = "▓" * bar_length

        table.add_row(
            f"{hour:02}:00",
            bar,
            format_time(usage)
        )

    return table


# DASHBOARD

def build_dashboard():

    summary = Table(
        title="TODAY"
    )

    summary.add_column("Metric")
    summary.add_column("Value")

    summary.add_row(
        "Productivity Score",
        f"{get_productivity_score()}%"
    )

    summary.add_row(
        "Active Time",
        format_time(
            get_total_active_time()
        )
    )

    summary.add_row(
        "Idle Time",
        format_time(
            get_total_idle_time()
        )
    )

    summary.add_row(
        "Coding Time",
        format_time(
            get_coding_time()
        )
    )

    apps = Table(
        title="TOP APPLICATIONS"
    )

    apps.add_column(
        "Application"
    )

    apps.add_column(
        "Time"
    )

    for app, duration in get_top_apps(8):

        apps.add_row(
            app,
            format_time(duration)
        )

    activities = Table(
        title="TOP ACTIVITIES"
    )

    activities.add_column(
        "Activity"
    )

    activities.add_column(
        "Time"
    )

    for title, duration in get_top_activities(8):

        activities.add_row(
            title[:60],
            format_time(duration)
        )

    return Group(
        summary,
        apps,
        activities,
        build_heatmap()
    )


def main():

    global current_app
    global current_title
    global tracking_start

    if not acquire_lock():

        print(
            "\nTracking is already running. Stop existing instance before starting a new instance."
        )

        return

    init_db()

    current_app = None
    current_title = None

    tracking_start = datetime.now()

    try:

        with Live(
            build_dashboard(),
            refresh_per_second=1
        ) as live:

            while True:

                idle_time = int(
                    get_idle_seconds()
                )

                # IDLE DETECTION

                if idle_time > IDLE_LIMIT:

                    if not current_state["is_idle"]:

                        save_current_session()

                        current_state[
                            "is_idle"
                        ] = True

                        current_state[
                            "idle_start"
                        ] = datetime.now()

                else:

                    if current_state["is_idle"]:

                        idle_end = datetime.now()

                        idle_duration = int(
                            (
                                idle_end
                                - current_state[
                                    "idle_start"
                                ]
                            ).total_seconds()
                        )

                        save_idle(
                            str(
                                current_state[
                                    "idle_start"
                                ]
                            ),
                            str(idle_end),
                            idle_duration
                        )

                        current_state[
                            "is_idle"
                        ] = False

                        tracking_start = datetime.now()

                # TRACK ACTIVE WINDOW

                if not current_state["is_idle"]:

                    window = get_active_window()

                    new_app = window["app"]

                    new_title = window["title"]

                    if current_app is None:

                        current_app = new_app

                        current_title = new_title

                        tracking_start = datetime.now()

                    elif new_app != current_app:

                        save_current_session()

                        current_app = new_app

                        current_title = new_title

                        tracking_start = datetime.now()

                    elapsed = int(
                        (
                            datetime.now()
                            - tracking_start
                        ).total_seconds()
                    )

                    if elapsed >= SAVE_INTERVAL:

                        save_current_session()

                        tracking_start = datetime.now()

                live.update(
                    build_dashboard()
                )

                time.sleep(1)

    except KeyboardInterrupt:

        save_current_session()

        print(
            "\nTracker stopped."
        )


if __name__ == "__main__":

    main()
    
    
