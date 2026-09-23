    def isin(self, values):
        """
        Compute boolean array of whether each index value is found in the
        passed set of values

        Parameters
        ----------
        values : set or sequence of values

        Returns
        -------
        is_contained : ndarray (boolean dtype)
        """
        if not isinstance(values, type(self)):
            try:
                values = type(self)(values)
            except ValueError:
                return self.astype(object).isin(values)

        return algorithms.isin(self.asi8, values.asi8)
