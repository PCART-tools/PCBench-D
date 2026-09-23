    def slice_shift(self, periods=1, axis=0, **kwds):
        """
        Equivalent to `shift` without copying data. The shifted data will
        not include the dropped periods and the shifted axis will be smaller
        than the original.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative

        Notes
        -----
        While the `slice_shift` is faster than `shift`, you may pay for it
        later during alignment.

        Returns
        -------
        shifted : same type as caller
        """
        if periods == 0:
            return self

        if periods > 0:
            vslicer = slice(None, -periods)
            islicer = slice(periods, None)
        else:
            vslicer = slice(-periods, None)
            islicer = slice(None, periods)

        new_obj = self._slice(vslicer, axis=axis)
        shifted_axis = self._get_axis(axis)[islicer]
        new_obj.set_axis(axis, shifted_axis)

        return new_obj.__finalize__(self)
