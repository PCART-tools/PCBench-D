def parse_http_date(date):
    """
    Parse a date format as specified by HTTP RFC7231 section 7.1.1.1.

    The three formats allowed by the RFC are accepted, even if only the first
    one is still in widespread use.

    Return an integer expressed in seconds since the epoch, in UTC.
    """
    # email.utils.parsedate() does the job for RFC1123 dates; unfortunately
    # RFC7231 makes it mandatory to support RFC850 dates too. So we roll
    # our own RFC-compliant parsing.
    for regex in RFC1123_DATE, RFC850_DATE, ASCTIME_DATE:
        m = regex.match(date)
        if m is not None:
            break
    else:
        raise ValueError("%r is not in a valid HTTP date format" % date)
    try:
        tz = datetime.timezone.utc
        year = int(m['year'])
        if year < 100:
            current_year = datetime.datetime.now(tz=tz).year
            current_century = current_year - (current_year % 100)
            if year - (current_year % 100) > 50:
                # year that appears to be more than 50 years in the future are
                # interpreted as representing the past.
                year += current_century - 100
            else:
                year += current_century
        month = MONTHS.index(m['mon'].lower()) + 1
        day = int(m['day'])
        hour = int(m['hour'])
        min = int(m['min'])
        sec = int(m['sec'])
        result = datetime.datetime(year, month, day, hour, min, sec, tzinfo=tz)
        return int(result.timestamp())
    except Exception as exc:
        raise ValueError("%r is not a valid date" % date) from exc
