    def __init__(self, t, fmt, tz=None):
        """
        Parameters
        ----------
        t : list of float
            A sequence of dates (floating point days).
        fmt : str
            A `~datetime.datetime.strftime` format string.
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.t = t
        self.fmt = fmt
        self.tz = tz
