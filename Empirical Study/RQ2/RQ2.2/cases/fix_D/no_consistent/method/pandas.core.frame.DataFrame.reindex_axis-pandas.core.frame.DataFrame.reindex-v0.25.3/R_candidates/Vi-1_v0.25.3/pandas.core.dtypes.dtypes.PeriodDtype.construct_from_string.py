    @classmethod
    def construct_from_string(cls, string):
        """
        Strict construction from a string, raise a TypeError if not
        possible
        """
        if (
            isinstance(string, str)
            and (string.startswith("period[") or string.startswith("Period["))
            or isinstance(string, ABCDateOffset)
        ):
            # do not parse string like U as period[U]
            # avoid tuple to be regarded as freq
            try:
                return cls(freq=string)
            except ValueError:
                pass
        raise TypeError("could not construct PeriodDtype")
