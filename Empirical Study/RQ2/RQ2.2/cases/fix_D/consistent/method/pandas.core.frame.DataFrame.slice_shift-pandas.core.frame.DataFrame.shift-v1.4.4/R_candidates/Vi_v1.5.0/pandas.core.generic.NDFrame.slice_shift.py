    @final
    def slice_shift(self: NDFrameT, periods: int = 1, axis=0) -> NDFrameT:
        """
        Equivalent to `shift` without copying data.

        .. deprecated:: 1.2.0
            slice_shift is deprecated,
            use DataFrame/Series.shift instead.

        The shifted data will not include the dropped periods and the
        shifted axis will be smaller than the original.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative.
        axis : {0 or 'index', 1 or 'columns', None}, default 0
            For `Series` this parameter is unused and defaults to 0.

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
        warnings.warn(
            msg, FutureWarning, stacklevel=find_stack_level(inspect.currentframe())
        )

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
        new_obj = new_obj.set_axis(shifted_axis, axis=axis, copy=False)
        return new_obj.__finalize__(self, method="slice_shift")
