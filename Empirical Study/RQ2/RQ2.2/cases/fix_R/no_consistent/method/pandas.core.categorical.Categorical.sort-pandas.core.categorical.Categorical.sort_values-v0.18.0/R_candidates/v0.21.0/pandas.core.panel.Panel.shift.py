    def shift(self, periods=1, freq=None, axis='major'):
        """
        Shift index by desired number of periods with an optional time freq.
        The shifted data will not include the dropped periods and the
        shifted axis will be smaller than the original. This is different
        from the behavior of DataFrame.shift()

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative
        freq : DateOffset, timedelta, or time rule string, optional
        axis : {'items', 'major', 'minor'} or {0, 1, 2}

        Returns
        -------
        shifted : Panel
        """
        if freq:
            return self.tshift(periods, freq, axis=axis)

        return super(Panel, self).slice_shift(periods, axis=axis)
