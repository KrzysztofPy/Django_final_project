from datetime import datetime


def current_date(request):
    ctx = {
        "now": datetime.now(),
        "version": "1.1",
    }
    return ctx
