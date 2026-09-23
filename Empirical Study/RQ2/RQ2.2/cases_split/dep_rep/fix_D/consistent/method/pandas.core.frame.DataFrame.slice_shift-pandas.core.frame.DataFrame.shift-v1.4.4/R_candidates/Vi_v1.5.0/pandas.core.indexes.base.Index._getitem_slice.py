    def _getitem_slice(self: _IndexT, slobj: slice) -> _IndexT:
        """
        Fastpath for __getitem__ when we know we have a slice.
        """
        res = self._data[slobj]
        return type(self)._simple_new(res, name=self._name)
