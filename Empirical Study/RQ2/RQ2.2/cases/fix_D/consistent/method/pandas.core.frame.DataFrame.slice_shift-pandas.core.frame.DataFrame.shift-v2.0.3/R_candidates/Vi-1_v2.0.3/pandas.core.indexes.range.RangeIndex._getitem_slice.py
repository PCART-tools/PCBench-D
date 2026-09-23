    def _getitem_slice(self: RangeIndex, slobj: slice) -> RangeIndex:
        """
        Fastpath for __getitem__ when we know we have a slice.
        """
        res = self._range[slobj]
        return type(self)._simple_new(res, name=self._name)
