    def _slice(self, slobj, axis=0, kind=None):
        """
        Construct a slice of this container.

        kind parameter is maintained for compatibility with Series slicing.

        """
        axis = self._get_block_manager_axis(axis)
        result = self._constructor(self._data.get_slice(slobj, axis=axis))

        # this could be a view
        # but only in a single-dtyped view slicable case
        is_copy = axis!=0 or result._is_view
        result._set_is_copy(self, copy=is_copy)
        return result
