    def _slice(self, slobj, axis=0, raise_on_error=False, typ=None):
        new_data = self._data.get_slice(slobj,
                                        axis=axis,
                                        raise_on_error=raise_on_error)
        return self._constructor(new_data)
