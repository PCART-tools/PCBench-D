    def __init__(self, t, fmt, tz=None):
        """
        *t* is a sequence of dates (floating point days).  *fmt* is a
        `~datetime.datetime.strftime` format string.
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.t = t
        self.fmt = fmt
        self.tz = tz
