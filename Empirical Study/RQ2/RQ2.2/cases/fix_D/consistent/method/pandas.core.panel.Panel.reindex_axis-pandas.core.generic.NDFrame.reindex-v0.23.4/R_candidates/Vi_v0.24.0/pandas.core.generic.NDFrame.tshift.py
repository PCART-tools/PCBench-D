    def tshift(self, periods=1, freq=None, axis=0):
        """
        Shift the time index, using the index's frequency if available.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative
        freq : DateOffset, timedelta, or time rule string, default None
            Increment to use from the tseries module or time rule (e.g. 'EOM')
        axis : int or basestring
            Corresponds to the axis that contains the Index

        Returns
        -------
        shifted : NDFrame

        Notes
        -----
        If freq is not specified then tries to use the freq or inferred_freq
        attributes of the index. If neither of those attributes exist, a
        ValueError is thrown
        """

        index = self._get_axis(axis)
        if freq is None:
            freq = getattr(index, 'freq', None)

        if freq is None:
            freq = getattr(index, 'inferred_freq', None)

        if freq is None:
            msg = 'Freq was not given and was not set in the index'
            raise ValueError(msg)

        if periods == 0:
            return self

        if isinstance(freq, string_types):
            freq = to_offset(freq)

        block_axis = self._get_block_manager_axis(axis)
        if isinstance(index, PeriodIndex):
            orig_freq = to_offset(index.freq)
            if freq == orig_freq:
                new_data = self._data.copy()
                new_data.axes[block_axis] = index.shift(periods)
            else:
                msg = ('Given freq %s does not match PeriodIndex freq %s' %
                       (freq.rule_code, orig_freq.rule_code))
                raise ValueError(msg)
        else:
            new_data = self._data.copy()
            new_data.axes[block_axis] = index.shift(periods, freq)

        return self._constructor(new_data).__finalize__(self)
