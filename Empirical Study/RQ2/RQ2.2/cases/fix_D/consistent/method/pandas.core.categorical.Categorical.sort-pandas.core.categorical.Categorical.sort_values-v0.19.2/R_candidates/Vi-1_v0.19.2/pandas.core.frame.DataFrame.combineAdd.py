    def combineAdd(self, other):
        """
        DEPRECATED. Use ``DataFrame.add(other, fill_value=0.)`` instead.

        Add two DataFrame objects and do not propagate
        NaN values, so if for a (column, time) one frame is missing a
        value, it will default to the other frame's value (which might
        be NaN as well)

        Parameters
        ----------
        other : DataFrame

        Returns
        -------
        DataFrame

        See also
        --------
        DataFrame.add

        """
        warnings.warn("'combineAdd' is deprecated. Use "
                      "'DataFrame.add(other, fill_value=0.)' instead",
                      FutureWarning, stacklevel=2)
        return self.add(other, fill_value=0.)
