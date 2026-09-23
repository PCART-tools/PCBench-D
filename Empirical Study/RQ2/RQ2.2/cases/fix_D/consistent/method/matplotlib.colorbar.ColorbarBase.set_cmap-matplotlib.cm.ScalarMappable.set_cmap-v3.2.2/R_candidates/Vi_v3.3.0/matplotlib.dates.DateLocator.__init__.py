    def __init__(self, tz=None):
        """
        Parameters
        ----------
        tz : `datetime.tzinfo`
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.tz = tz
