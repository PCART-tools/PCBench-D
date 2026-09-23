    def mean(self, *, skipna: bool = True, axis: int | None = 0):
        """
        Return the mean value of the Array.

        .. versionadded:: 0.25.0

        Parameters
        ----------
        skipna : bool, default True
            Whether to ignore any NaT elements.
        axis : int, optional, default 0

        Returns
        -------
        scalar
            Timestamp or Timedelta.

        See Also
        --------
        numpy.ndarray.mean : Returns the average of array elements along a given axis.
        Series.mean : Return the mean value in a Series.

        Notes
        -----
        mean is only defined for Datetime and Timedelta dtypes, not for Period.
        """
        if is_period_dtype(self.dtype):
            # See discussion in GH#24757
            raise TypeError(
                f"mean is not implemented for {type(self).__name__} since the "
                "meaning is ambiguous.  An alternative is "
                "obj.to_timestamp(how='start').mean()"
            )

        result = nanops.nanmean(
            self._ndarray, axis=axis, skipna=skipna, mask=self.isna()
        )
        return self._wrap_reduction_result(axis, result)
