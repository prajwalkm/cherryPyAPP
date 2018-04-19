from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    "poll_SO": {
        "task": "tasks.getBhavData",
        "schedule": timedelta(seconds=30),
        "args": []
    }
}

