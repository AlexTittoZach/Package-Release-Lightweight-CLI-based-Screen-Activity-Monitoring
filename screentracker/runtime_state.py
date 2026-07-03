from datetime import datetime


current_state = {

    "hourly_usage": {
         hour: 0
        for hour in range(24)
    },


    "current_app": "",

    "current_title": "",

    "activity_start": datetime.now(),

    "current_activity_time": 0,

    # -------------------------
    # Today's Counters
    # -------------------------

    "active_time_today": 0,

    "idle_time_today": 0,

    # -------------------------
    # Idle Tracking
    # -------------------------

    "is_idle": False,

    "idle_start": None,

    "current_idle_time": 0,

    # -------------------------
    # Runtime
    # -------------------------

    "started_at": datetime.now()
}