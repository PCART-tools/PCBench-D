    def __init__(self, fmt, tz=None):
        """
        *fmt* is a :func:`strftime` format string; *tz* is the
         :class:`tzinfo` instance.
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.fmt = fmt
        self.tz = tz
