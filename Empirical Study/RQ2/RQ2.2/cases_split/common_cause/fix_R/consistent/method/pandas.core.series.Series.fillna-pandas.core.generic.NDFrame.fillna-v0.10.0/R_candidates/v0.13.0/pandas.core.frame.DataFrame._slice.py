    def _slice(self, slobj, axis=0, raise_on_error=False, typ=None):
        axis = self._get_block_manager_axis(axis)
        new_data = self._data.get_slice(
            slobj, axis=axis, raise_on_error=raise_on_error)
        return self._constructor(new_data)
