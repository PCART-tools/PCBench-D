    def major_xs(self, key, copy=None):
        """
        Return slice of panel along major axis

        Parameters
        ----------
        key : object
            Major axis label
        copy : boolean [deprecated]
            Whether to make a copy of the data

        Returns
        -------
        y : DataFrame
            index -> minor axis, columns -> items

        Notes
        -----
        major_xs is only for getting, not setting values.

        MultiIndex Slicers is a generic way to get/set values on any level or levels
        it is a superset of major_xs functionality, see :ref:`MultiIndex Slicers <advanced.mi_slicers>`

        """
        if copy is not None:
            warnings.warn("copy keyword is deprecated, "
                          "default is to return a copy or a view if possible")

        return self.xs(key, axis=self._AXIS_LEN - 2)
