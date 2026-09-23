    def __init__(self, fmt, tz=None):
        """
        Parameters
        ----------
        fmt : str
            `strftime` format string
        tz : `tzinfo`
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.fmt = fmt
        self.tz = tz
