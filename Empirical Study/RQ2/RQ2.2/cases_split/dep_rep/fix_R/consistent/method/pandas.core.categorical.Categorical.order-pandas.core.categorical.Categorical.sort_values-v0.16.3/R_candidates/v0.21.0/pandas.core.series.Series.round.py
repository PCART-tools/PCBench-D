    def round(self, decimals=0, *args, **kwargs):
        """
        Round each value in a Series to the given number of decimals.

        Parameters
        ----------
        decimals : int
            Number of decimal places to round to (default: 0).
            If decimals is negative, it specifies the number of
            positions to the left of the decimal point.

        Returns
        -------
        Series object

        See Also
        --------
        numpy.around
        DataFrame.round

        """
        nv.validate_round(args, kwargs)
        result = _values_from_object(self).round(decimals)
        result = self._constructor(result, index=self.index).__finalize__(self)

        return result
