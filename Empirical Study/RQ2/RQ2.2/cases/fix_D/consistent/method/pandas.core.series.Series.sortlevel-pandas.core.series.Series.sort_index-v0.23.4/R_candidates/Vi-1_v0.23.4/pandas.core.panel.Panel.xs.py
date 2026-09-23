    def xs(self, key, axis=1):
        """
        Return slice of panel along selected axis

        Parameters
        ----------
        key : object
            Label
        axis : {'items', 'major', 'minor}, default 1/'major'

        Returns
        -------
        y : ndim(self)-1

        Notes
        -----
        xs is only for getting, not setting values.

        MultiIndex Slicers is a generic way to get/set values on any level or
        levels and is a superset of xs functionality, see
        :ref:`MultiIndex Slicers <advanced.mi_slicers>`

        """
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
