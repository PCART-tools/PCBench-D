    def mean(self, skipna=True):
        """
        Return the mean value of the Array.

        .. versionadded:: 0.25.0

        Parameters
        ----------
        skipna : bool, default True
            Whether to ignore any NaT elements.

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
        if is_period_dtype(self):
            # See discussion in GH#24757
            raise TypeError(
                f"mean is not implemented for {type(self).__name__} since the "
                "meaning is ambiguous.  An alternative is "
                "obj.to_timestamp(how='start').mean()"
            )

        mask = self.isna()
        if skipna:
            values = self[~mask]
        elif mask.any():
            return NaT
        else:
            values = self

        if not len(values):
            # short-circuit for empty max / min
            return NaT

        result = nanops.nanmean(values.view("i8"), skipna=skipna)
        # Don't have to worry about NA `result`, since no NA went in.
        return self._box_func(result)
