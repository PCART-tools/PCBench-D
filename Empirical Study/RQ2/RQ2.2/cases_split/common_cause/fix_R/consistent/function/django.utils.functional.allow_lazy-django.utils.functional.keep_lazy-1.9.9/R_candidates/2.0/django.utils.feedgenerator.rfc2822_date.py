def rfc2822_date(date):
    # We can't use strftime() because it produces locale-dependent results, so
    # we have to map english month and day names manually
    months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',)
    days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    # Support datetime objects older than 1900
    date = datetime_safe.new_datetime(date)
    # Timezone aware formatting. email.utils.formatdate() isn't tz aware.
    dow = days[date.weekday()]
    month = months[date.month - 1]
    time_str = date.strftime('%s, %%d %s %%Y %%H:%%M:%%S ' % (dow, month))
    offset = date.utcoffset()
    # Historically, this function assumes that naive datetimes are in UTC.
    if offset is None:
        return time_str + '-0000'
    else:
        timezone = (offset.days * 24 * 60) + (offset.seconds // 60)
        hour, minute = divmod(timezone, 60)
        return time_str + '%+03d%02d' % (hour, minute)
