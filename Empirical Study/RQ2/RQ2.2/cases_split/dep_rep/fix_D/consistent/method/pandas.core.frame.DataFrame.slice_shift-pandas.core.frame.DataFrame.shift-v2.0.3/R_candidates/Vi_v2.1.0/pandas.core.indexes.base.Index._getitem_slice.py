    def _getitem_slice(self, slobj: slice) -> Self:
        """
        Fastpath for __getitem__ when we know we have a slice.
        """
        res = self._data[slobj]
        result = type(self)._simple_new(res, name=self._name, refs=self._references)
        if "_engine" in self._cache:
            reverse = slobj.step is not None and slobj.step < 0
            result._engine._update_from_sliced(self._engine, reverse=reverse)  # type: ignore[union-attr]  # noqa: E501

        return result
