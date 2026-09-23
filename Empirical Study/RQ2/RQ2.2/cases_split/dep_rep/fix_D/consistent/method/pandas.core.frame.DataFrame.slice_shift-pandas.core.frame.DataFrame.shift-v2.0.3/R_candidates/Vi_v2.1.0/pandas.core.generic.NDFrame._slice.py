    def _slice(self, slobj: slice, axis: AxisInt = 0) -> Self:
        """
        Construct a slice of this container.

        Slicing with this method is *always* positional.
        """
        assert isinstance(slobj, slice), type(slobj)
        axis = self._get_block_manager_axis(axis)
        new_mgr = self._mgr.get_slice(slobj, axis=axis)
        result = self._constructor_from_mgr(new_mgr, axes=new_mgr.axes)
        result = result.__finalize__(self)

        # this could be a view
        # but only in a single-dtyped view sliceable case
        is_copy = axis != 0 or result._is_view
        result._set_is_copy(self, copy=is_copy)
        return result
