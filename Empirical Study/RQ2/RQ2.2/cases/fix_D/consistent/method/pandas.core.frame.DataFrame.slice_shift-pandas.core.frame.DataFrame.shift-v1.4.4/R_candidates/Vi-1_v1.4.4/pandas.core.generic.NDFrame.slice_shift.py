    @final
    def slice_shift(self: NDFrameT, periods: int = 1, axis=0) -> NDFrameT:
        """
        Equivalent to `shift` without copying data.
        The shifted data will not include the dropped periods and the
        shifted axis will be smaller than the original.

        .. deprecated:: 1.2.0
            slice_shift is deprecated,
            use DataFrame/Series.shift instead.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative.

        Returns
        -------
        shifted : same type as caller

        Notes
        -----
        While the `slice_shift` is faster than `shift`, you may pay for it
        later during alignment.
        """

        msg = (
            "The 'slice_shift' method is deprecated "
            "and will be removed in a future version. "
            "You can use DataFrame/Series.shift instead."
        )
        warnings.warn(msg, FutureWarning, stacklevel=find_stack_level())

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
        new_obj.set_axis(shifted_axis, axis=axis, inplace=True)

        return new_obj.__finalize__(self, method="slice_shift")
