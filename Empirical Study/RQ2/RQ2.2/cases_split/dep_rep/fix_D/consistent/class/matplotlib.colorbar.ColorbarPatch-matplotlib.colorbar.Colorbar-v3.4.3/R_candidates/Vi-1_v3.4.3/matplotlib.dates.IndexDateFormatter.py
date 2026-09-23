@_api.deprecated("3.3")
class IndexDateFormatter(ticker.Formatter):
    """Use with `.IndexLocator` to cycle format strings by index."""

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

    def __call__(self, x, pos=0):
        """Return the label for time *x* at position *pos*."""
        ind = int(round(x))
        if ind >= len(self.t) or ind <= 0:
            return ''
        return num2date(self.t[ind], self.tz).strftime(self.fmt)
