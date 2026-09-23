    def __init__(self, tz=None):
        """
        *tz* is a :class:`tzinfo` instance.
        """
        if tz is None:
            tz = _get_rc_timezone()
        self.tz = tz
