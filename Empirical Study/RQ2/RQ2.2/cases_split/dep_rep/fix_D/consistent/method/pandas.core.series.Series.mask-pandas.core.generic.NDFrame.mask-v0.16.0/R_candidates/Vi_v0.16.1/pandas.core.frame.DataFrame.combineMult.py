    def combineMult(self, other):
        """
        Multiply two DataFrame objects and do not propagate NaN values, so if
        for a (column, time) one frame is missing a value, it will default to
        the other frame's value (which might be NaN as well)

        Parameters
        ----------
        other : DataFrame

        Returns
        -------
        DataFrame
        """
        return self.mul(other, fill_value=1.)
