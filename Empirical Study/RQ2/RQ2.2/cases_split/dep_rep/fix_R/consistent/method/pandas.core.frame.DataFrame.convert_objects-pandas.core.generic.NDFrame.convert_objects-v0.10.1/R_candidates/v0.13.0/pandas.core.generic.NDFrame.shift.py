    def shift(self, periods=1, freq=None, axis=0, **kwds):
        """
        Shift index by desired number of periods with an optional time freq

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative
        freq : DateOffset, timedelta, or time rule string, optional
            Increment to use from datetools module or time rule (e.g. 'EOM')

        Notes
        -----
        If freq is specified then the index values are shifted but the data
        if not realigned

        Returns
        -------
        shifted : same type as caller
        """
        if periods == 0:
            return self

        if freq is None and not len(kwds):
            block_axis = self._get_block_manager_axis(axis)
            indexer = com._shift_indexer(len(self), periods)
            new_data = self._data.shift(indexer, periods, axis=block_axis)
        else:
            return self.tshift(periods, freq, **kwds)

        return self._constructor(new_data).__finalize__(self)
