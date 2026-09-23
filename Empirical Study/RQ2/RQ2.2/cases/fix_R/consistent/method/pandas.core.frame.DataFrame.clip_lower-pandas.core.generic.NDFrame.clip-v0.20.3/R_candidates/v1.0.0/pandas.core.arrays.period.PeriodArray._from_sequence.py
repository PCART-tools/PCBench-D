    @classmethod
    def _from_sequence(
        cls,
        scalars: Sequence[Optional[Period]],
        dtype: Optional[PeriodDtype] = None,
        copy: bool = False,
    ) -> ABCPeriodArray:
        if dtype:
            freq = dtype.freq
        else:
            freq = None

        if isinstance(scalars, cls):
            validate_dtype_freq(scalars.dtype, freq)
            if copy:
                scalars = scalars.copy()
            return scalars

        periods = np.asarray(scalars, dtype=object)
        if copy:
            periods = periods.copy()

        freq = freq or libperiod.extract_freq(periods)
        ordinals = libperiod.extract_ordinals(periods, freq)
        return cls(ordinals, freq=freq)
