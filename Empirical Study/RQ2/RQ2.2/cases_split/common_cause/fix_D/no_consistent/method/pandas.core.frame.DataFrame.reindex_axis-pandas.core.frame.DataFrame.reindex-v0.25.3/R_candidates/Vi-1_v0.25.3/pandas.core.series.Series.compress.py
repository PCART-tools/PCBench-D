    def compress(self, condition, *args, **kwargs):
        """
        Return selected slices of an array along given axis as a Series.

        .. deprecated:: 0.24.0

        Returns
        -------
        Series
            Series without the slices for which condition is false.

        See Also
        --------
        numpy.ndarray.compress
        """
        msg = (
            "Series.compress(condition) is deprecated. "
            "Use 'Series[condition]' or "
            "'np.asarray(series).compress(condition)' instead."
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)
        nv.validate_compress(args, kwargs)
        return self[condition]
