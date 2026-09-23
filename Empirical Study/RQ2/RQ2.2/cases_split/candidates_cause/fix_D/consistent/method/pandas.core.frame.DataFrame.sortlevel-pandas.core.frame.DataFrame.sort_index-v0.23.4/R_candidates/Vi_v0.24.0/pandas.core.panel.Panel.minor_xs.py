    def minor_xs(self, key):
        """
        Return slice of panel along minor axis.

        Parameters
        ----------
        key : object
            Minor axis label

        Returns
        -------
        y : DataFrame
            index -> major axis, columns -> items

        Notes
        -----
        minor_xs is only for getting, not setting values.

        MultiIndex Slicers is a generic way to get/set values on any level or
        levels and is a superset of minor_xs functionality, see
        :ref:`MultiIndex Slicers <advanced.mi_slicers>`
        """
        return self.xs(key, axis=self._AXIS_LEN - 1)
