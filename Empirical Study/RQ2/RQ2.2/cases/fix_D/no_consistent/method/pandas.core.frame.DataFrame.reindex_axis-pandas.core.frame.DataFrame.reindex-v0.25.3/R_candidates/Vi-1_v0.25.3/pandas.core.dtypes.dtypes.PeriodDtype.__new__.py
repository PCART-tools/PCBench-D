    def __new__(cls, freq=None):
        """
        Parameters
        ----------
        freq : frequency
        """

        if isinstance(freq, PeriodDtype):
            return freq

        elif freq is None:
            # empty constructor for pickle compat
            u = object.__new__(cls)
            u._freq = None
            return u

        if not isinstance(freq, ABCDateOffset):
            freq = cls._parse_dtype_strict(freq)

        try:
            return cls._cache[freq.freqstr]
        except KeyError:
            u = object.__new__(cls)
            u._freq = freq
            cls._cache[freq.freqstr] = u
            return u
