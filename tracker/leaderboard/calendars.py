import calendar
from datetime import date

from django.utils import timezone


def elimination_calendar(tracking, entries):
    """One dict per month; each cell holds the entries (eliminations) on that local day."""
    by_day = {}
    for e in entries:
        by_day.setdefault(timezone.localtime(e.occurred_at).date(), []).append(e)

    start = tracking.start_date
    end = tracking.end_date or date(
        start.year, start.month, calendar.monthrange(start.year, start.month)[1]
    )
    if by_day:  # never hide an elimination that falls outside the configured range
        start, end = min(start, min(by_day)), max(end, max(by_day))

    cal = calendar.Calendar(firstweekday=0)  # weeks start on Monday
    months, (y, m) = [], (start.year, start.month)
    while (y, m) <= (end.year, end.month):
        weeks = [
            [
                {
                    "date": d,
                    "in_month": d.month == m,
                    "in_range": start <= d <= end,
                    "entries": by_day.get(d, []),
                }
                for d in week
            ]
            for week in cal.monthdatescalendar(y, m)
        ]
        months.append({"label": date(y, m, 1), "weeks": weeks})
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return months
