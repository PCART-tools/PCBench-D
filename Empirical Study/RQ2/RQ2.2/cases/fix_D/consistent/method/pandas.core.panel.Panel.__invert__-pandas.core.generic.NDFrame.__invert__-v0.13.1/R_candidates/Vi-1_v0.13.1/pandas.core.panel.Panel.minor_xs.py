    def minor_xs(self, key, copy=True):
        """
        Return slice of panel along minor axis

        Parameters
        ----------
        key : object
            Minor axis label
        copy : boolean, default True
            Copy data

        Returns
        -------
        y : DataFrame
            index -> major axis, columns -> items
        """
        return self.xs(key, axis=self._AXIS_LEN - 1, copy=copy)
