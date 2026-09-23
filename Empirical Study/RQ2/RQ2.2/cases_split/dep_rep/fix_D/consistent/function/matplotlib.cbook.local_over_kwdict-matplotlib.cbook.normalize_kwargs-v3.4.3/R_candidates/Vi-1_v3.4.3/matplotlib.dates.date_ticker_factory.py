def date_ticker_factory(span, tz=None, numticks=5):
    """
    Create a date locator with *numticks* (approx) and a date formatter
    for *span* in days.  Return value is (locator, formatter).
    """

    if span == 0:
        span = 1 / HOURS_PER_DAY

    mins = span * MINUTES_PER_DAY
    hrs = span * HOURS_PER_DAY
    days = span
    wks = span / DAYS_PER_WEEK
    months = span / DAYS_PER_MONTH      # Approx
    years = span / DAYS_PER_YEAR        # Approx

    if years > numticks:
        locator = YearLocator(int(years / numticks), tz=tz)  # define
        fmt = '%Y'
    elif months > numticks:
        locator = MonthLocator(tz=tz)
        fmt = '%b %Y'
    elif wks > numticks:
        locator = WeekdayLocator(tz=tz)
        fmt = '%a, %b %d'
    elif days > numticks:
        locator = DayLocator(interval=math.ceil(days / numticks), tz=tz)
        fmt = '%b %d'
    elif hrs > numticks:
        locator = HourLocator(interval=math.ceil(hrs / numticks), tz=tz)
        fmt = '%H:%M\n%b %d'
    elif mins > numticks:
        locator = MinuteLocator(interval=math.ceil(mins / numticks), tz=tz)
        fmt = '%H:%M:%S'
    else:
        locator = MinuteLocator(tz=tz)
        fmt = '%H:%M:%S'

    formatter = DateFormatter(fmt, tz=tz)
    return locator, formatter
