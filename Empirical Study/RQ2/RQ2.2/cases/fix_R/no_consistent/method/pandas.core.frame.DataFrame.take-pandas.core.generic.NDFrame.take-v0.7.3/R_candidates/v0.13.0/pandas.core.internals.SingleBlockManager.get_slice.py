    def get_slice(self, slobj, raise_on_error=False):
        if raise_on_error:
            _check_slice_bounds(slobj, self.index)
        return self.__class__(self._block._slice(slobj),
                              self.index._getitem_slice(slobj), fastpath=True)
