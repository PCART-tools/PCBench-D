    def __init__(self, fmt, tz=None):
        """
        Parameters
        ----------
        fmt : str
            `~datetime.datetime.strftime` format string
        tz : `datetime.tzinfo`, default: :rc:`timezone`
            Ticks timezone.
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.fmt = fmt
        self.tz = tz
