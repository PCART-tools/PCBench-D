    @classmethod
    def construct_from_string(cls, string):
        """
        attempt to construct this type from a string, raise a TypeError
        if its not possible
        """
        from pandas.tseries.offsets import DateOffset
        if isinstance(string, (compat.string_types, DateOffset)):
            # avoid tuple to be regarded as freq
            try:
                return cls(freq=string)
            except ValueError:
                pass
        raise TypeError("could not construct PeriodDtype")
