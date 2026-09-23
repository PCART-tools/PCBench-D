    @final
    def tshift(self: NDFrameT, periods: int = 1, freq=None, axis: Axis = 0) -> NDFrameT:
        """
        Shift the time index, using the index's frequency if available.

        .. deprecated:: 1.1.0
            Use `shift` instead.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative.
        freq : DateOffset, timedelta, or str, default None
            Increment to use from the tseries module
            or time rule expressed as a string (e.g. 'EOM').
        axis : {0 or ‘index’, 1 or ‘columns’, None}, default 0
            Corresponds to the axis that contains the Index.

        Returns
        -------
        shifted : Series/DataFrame

        Notes
        -----
        If freq is not specified then tries to use the freq or inferred_freq
        attributes of the index. If neither of those attributes exist, a
        ValueError is thrown
        """
        warnings.warn(
            (
                "tshift is deprecated and will be removed in a future version. "
                "Please use shift instead."
            ),
            FutureWarning,
            stacklevel=find_stack_level(),
        )

        if freq is None:
            freq = "infer"

        return self.shift(periods, freq, axis)
