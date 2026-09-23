    def _slice(self, slobj, axis=0, typ=None):
        """
        Construct a slice of this container.

        typ parameter is maintained for compatibility with Series slicing.

        """
        axis = self._get_block_manager_axis(axis)
        return self._constructor(self._data.get_slice(slobj, axis=axis))
