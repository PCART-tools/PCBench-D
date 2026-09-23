    def tshift(self, periods=1, freq=None, axis=0, **kwargs):
        """
        Shift the time index, using the index's frequency if available

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative
        freq : DateOffset, timedelta, or time rule string, default None
            Increment to use from datetools module or time rule (e.g. 'EOM')
        axis : int or basestring
            Corresponds to the axis that contains the Index

        Notes
        -----
        If freq is not specified then tries to use the freq or inferred_freq
        attributes of the index. If neither of those attributes exist, a
        ValueError is thrown

        Returns
        -------
        shifted : NDFrame
        """
        from pandas.core.datetools import _resolve_offset

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

        offset = _resolve_offset(freq, kwargs)

        if isinstance(offset, string_types):
            offset = datetools.to_offset(offset)

        block_axis = self._get_block_manager_axis(axis)
        if isinstance(index, PeriodIndex):
            orig_offset = datetools.to_offset(index.freq)
            if offset == orig_offset:
                new_data = self._data.copy()
                new_data.axes[block_axis] = index.shift(periods)
            else:
                msg = ('Given freq %s does not match PeriodIndex freq %s' %
                       (offset.rule_code, orig_offset.rule_code))
                raise ValueError(msg)
        else:
            new_data = self._data.copy()
            new_data.axes[block_axis] = index.shift(periods, offset)

        return self._constructor(new_data).__finalize__(self)
