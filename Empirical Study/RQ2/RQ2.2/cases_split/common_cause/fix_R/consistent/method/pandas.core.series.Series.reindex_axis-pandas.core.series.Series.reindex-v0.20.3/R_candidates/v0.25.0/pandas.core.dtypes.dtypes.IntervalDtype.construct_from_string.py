    @classmethod
    def construct_from_string(cls, string):
        """
        attempt to construct this type from a string, raise a TypeError
        if its not possible
        """
        if not isinstance(string, str):
            msg = "a string needs to be passed, got type {typ}"
            raise TypeError(msg.format(typ=type(string)))

        if string.lower() == "interval" or cls._match.search(string) is not None:
            return cls(string)

        msg = (
            "Incorrectly formatted string passed to constructor. "
            "Valid formats include Interval or Interval[dtype] "
            "where dtype is numeric, datetime, or timedelta"
        )
        raise TypeError(msg)
