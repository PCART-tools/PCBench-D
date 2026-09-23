    def major_xs(self, key):
        """
        Return slice of panel along major axis.

        Parameters
        ----------
        key : object
            Major axis label

        Returns
        -------
        y : DataFrame
            index -> minor axis, columns -> items

        Notes
        -----
        major_xs is only for getting, not setting values.

        MultiIndex Slicers is a generic way to get/set values on any level or
        levels and is a superset of major_xs functionality, see
        :ref:`MultiIndex Slicers <advanced.mi_slicers>`
        """
        return self.xs(key, axis=self._AXIS_LEN - 2)
