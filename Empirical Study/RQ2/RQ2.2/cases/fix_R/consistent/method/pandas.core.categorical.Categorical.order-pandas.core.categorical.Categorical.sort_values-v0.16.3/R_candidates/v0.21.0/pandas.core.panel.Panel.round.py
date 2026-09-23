    def round(self, decimals=0, *args, **kwargs):
        """
        Round each value in Panel to a specified number of decimal places.

        .. versionadded:: 0.18.0

        Parameters
        ----------
        decimals : int
            Number of decimal places to round to (default: 0).
            If decimals is negative, it specifies the number of
            positions to the left of the decimal point.

        Returns
        -------
        Panel object

        See Also
        --------
        numpy.around
        """
        nv.validate_round(args, kwargs)

        if is_integer(decimals):
            result = np.apply_along_axis(np.round, 0, self.values)
            return self._wrap_result(result, axis=0)
        raise TypeError("decimals must be an integer")
