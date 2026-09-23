    @classmethod
    def _from_sequence(
        cls: type[PeriodArray],
        scalars: Sequence[Period | None] | AnyArrayLike,
        *,
        dtype: Dtype | None = None,
        copy: bool = False,
    ) -> PeriodArray:
        if dtype and isinstance(dtype, PeriodDtype):
            freq = dtype.freq
        else:
            freq = None

        if isinstance(scalars, cls):
            validate_dtype_freq(scalars.dtype, freq)
            if copy:
                scalars = scalars.copy()
            return scalars

        periods = np.asarray(scalars, dtype=object)

        freq = freq or libperiod.extract_freq(periods)
        ordinals = libperiod.extract_ordinals(periods, freq)
        return cls(ordinals, freq=freq)
