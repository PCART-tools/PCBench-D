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
            # -10_000 corresponds to PeriodDtypeCode.UNDEFINED
            u = PeriodDtypeBase.__new__(cls, -10_000)
            u._freq = None
            return u

        if not isinstance(freq, BaseOffset):
            freq = cls._parse_dtype_strict(freq)

        try:
            return cls._cache_dtypes[freq.freqstr]
        except KeyError:
            dtype_code = freq._period_dtype_code
            u = PeriodDtypeBase.__new__(cls, dtype_code)
            u._freq = freq
            cls._cache_dtypes[freq.freqstr] = u
            return u
