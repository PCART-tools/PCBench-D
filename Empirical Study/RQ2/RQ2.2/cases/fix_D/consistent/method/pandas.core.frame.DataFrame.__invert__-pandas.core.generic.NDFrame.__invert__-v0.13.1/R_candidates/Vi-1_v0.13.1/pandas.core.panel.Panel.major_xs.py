    def major_xs(self, key, copy=True):
        """
        Return slice of panel along major axis

        Parameters
        ----------
        key : object
            Major axis label
        copy : boolean, default True
            Copy data

        Returns
        -------
        y : DataFrame
            index -> minor axis, columns -> items
        """
        return self.xs(key, axis=self._AXIS_LEN - 2, copy=copy)
