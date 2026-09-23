    def shift(self, periods=1, freq=None, axis=0, **kwargs):
        """
        Shift index by desired number of periods with an optional time freq

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative
        freq : DateOffset, timedelta, or time rule string, optional
            Increment to use from datetools module or time rule (e.g. 'EOM').
            See Notes.

        Notes
        -----
        If freq is specified then the index values are shifted but the data
        is not realigned. That is, use freq if you would like to extend the
        index when shifting and preserve the original data.

        Returns
        -------
        shifted : same type as caller
        """
        if periods == 0:
            return self

        block_axis = self._get_block_manager_axis(axis)
        if freq is None and not len(kwargs):
            new_data = self._data.shift(periods=periods, axis=block_axis)
        else:
            return self.tshift(periods, freq, **kwargs)

        return self._constructor(new_data).__finalize__(self)
