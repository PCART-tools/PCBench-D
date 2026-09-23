    def get_slice(self, slobj, axis=0):
        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        return self.__class__(
            self._block._slice(slobj), self.index[slobj], fastpath=True
        )
