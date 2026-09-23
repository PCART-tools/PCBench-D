    def combineMult(self, other):
        """
        DEPRECATED. Use ``DataFrame.mul(other, fill_value=1.)`` instead.

        Multiply two DataFrame objects and do not propagate NaN values, so if
        for a (column, time) one frame is missing a value, it will default to
        the other frame's value (which might be NaN as well)

        Parameters
        ----------
        other : DataFrame

        Returns
        -------
        DataFrame

        See also
        --------
        DataFrame.mul

        """
        warnings.warn("'combineMult' is deprecated. Use "
                      "'DataFrame.mul(other, fill_value=1.)' instead",
                      FutureWarning, stacklevel=2)
        return self.mul(other, fill_value=1.)
