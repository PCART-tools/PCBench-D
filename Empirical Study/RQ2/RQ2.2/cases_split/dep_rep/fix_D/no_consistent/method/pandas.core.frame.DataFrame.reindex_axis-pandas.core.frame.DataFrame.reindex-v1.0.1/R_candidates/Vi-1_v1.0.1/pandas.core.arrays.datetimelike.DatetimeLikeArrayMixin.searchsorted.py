    def searchsorted(self, value, side="left", sorter=None):
        """
        Find indices where elements should be inserted to maintain order.

        Find the indices into a sorted array `self` such that, if the
        corresponding elements in `value` were inserted before the indices,
        the order of `self` would be preserved.

        Parameters
        ----------
        value : array_like
            Values to insert into `self`.
        side : {'left', 'right'}, optional
            If 'left', the index of the first suitable location found is given.
            If 'right', return the last such index.  If there is no suitable
            index, return either 0 or N (where N is the length of `self`).
        sorter : 1-D array_like, optional
            Optional array of integer indices that sort `self` into ascending
            order. They are typically the result of ``np.argsort``.

        Returns
        -------
        indices : array of ints
            Array of insertion points with the same shape as `value`.
        """
        if isinstance(value, str):
            value = self._scalar_from_string(value)

        if not (isinstance(value, (self._scalar_type, type(self))) or isna(value)):
            raise ValueError(f"Unexpected type for 'value': {type(value)}")

        self._check_compatible_with(value)
        if isinstance(value, type(self)):
            value = value.asi8
        else:
            value = self._unbox_scalar(value)

        return self.asi8.searchsorted(value, side=side, sorter=sorter)
