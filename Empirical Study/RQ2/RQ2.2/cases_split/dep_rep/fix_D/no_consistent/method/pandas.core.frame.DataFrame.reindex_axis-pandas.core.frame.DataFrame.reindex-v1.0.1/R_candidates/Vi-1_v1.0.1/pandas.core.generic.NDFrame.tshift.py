    def tshift(
        self: FrameOrSeries, periods: int = 1, freq=None, axis=0
    ) -> FrameOrSeries:
        """
        Shift the time index, using the index's frequency if available.

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

        index = self._get_axis(axis)
        if freq is None:
            freq = getattr(index, "freq", None)

        if freq is None:
            freq = getattr(index, "inferred_freq", None)

        if freq is None:
            msg = "Freq was not given and was not set in the index"
            raise ValueError(msg)

        if periods == 0:
            return self

        if isinstance(freq, str):
            freq = to_offset(freq)

        block_axis = self._get_block_manager_axis(axis)
        if isinstance(index, PeriodIndex):
            orig_freq = to_offset(index.freq)
            if freq == orig_freq:
                new_data = self._data.copy()
                new_data.axes[block_axis] = index.shift(periods)
            elif orig_freq is not None:
                msg = (
                    f"Given freq {freq.rule_code} does not match"
                    f" PeriodIndex freq {orig_freq.rule_code}"
                )
                raise ValueError(msg)
        else:
            new_data = self._data.copy()
            new_data.axes[block_axis] = index.shift(periods, freq)

        return self._constructor(new_data).__finalize__(self)
