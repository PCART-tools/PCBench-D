    def xs(self, key, axis=1, copy=None):
        """
        Return slice of panel along selected axis

        Parameters
        ----------
        key : object
            Label
        axis : {'items', 'major', 'minor}, default 1/'major'
        copy : boolean [deprecated]
            Whether to make a copy of the data

        Returns
        -------
        y : ndim(self)-1

        Notes
        -----
        xs is only for getting, not setting values.

        MultiIndex Slicers is a generic way to get/set values on any level or levels
        it is a superset of xs functionality, see :ref:`MultiIndex Slicers <indexing.mi_slicers>`

        """
        if copy is not None:
            warnings.warn("copy keyword is deprecated, "
                          "default is to return a copy or a view if possible")

        axis = self._get_axis_number(axis)
        if axis == 0:
            return self[key]

        self._consolidate_inplace()
        axis_number = self._get_axis_number(axis)
        new_data = self._data.xs(key, axis=axis_number, copy=False)
        result = self._construct_return_type(new_data)
        copy = new_data.is_mixed_type
        result._set_is_copy(self, copy=copy)
        return result
