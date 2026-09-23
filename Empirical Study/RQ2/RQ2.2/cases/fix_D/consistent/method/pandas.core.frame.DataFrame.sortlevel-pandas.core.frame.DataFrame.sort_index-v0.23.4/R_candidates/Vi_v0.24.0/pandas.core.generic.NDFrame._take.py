    def _take(self, indices, axis=0, is_copy=True):
        """
        Return the elements in the given *positional* indices along an axis.

        This means that we are not indexing according to actual values in
        the index attribute of the object. We are indexing according to the
        actual position of the element in the object.

        This is the internal version of ``.take()`` and will contain a wider
        selection of parameters useful for internal use but not as suitable
        for public usage.

        Parameters
        ----------
        indices : array-like
            An array of ints indicating which positions to take.
        axis : int, default 0
            The axis on which to select elements. "0" means that we are
            selecting rows, "1" means that we are selecting columns, etc.
        is_copy : bool, default True
            Whether to return a copy of the original object or not.

        Returns
        -------
        taken : same type as caller
            An array-like containing the elements taken from the object.

        See Also
        --------
        numpy.ndarray.take
        numpy.take
        """
        self._consolidate_inplace()

        new_data = self._data.take(indices,
                                   axis=self._get_block_manager_axis(axis),
                                   verify=True)
        result = self._constructor(new_data).__finalize__(self)

        # Maybe set copy if we didn't actually change the index.
        if is_copy:
            if not result._get_axis(axis).equals(self._get_axis(axis)):
                result._set_is_copy(self)

        return result
