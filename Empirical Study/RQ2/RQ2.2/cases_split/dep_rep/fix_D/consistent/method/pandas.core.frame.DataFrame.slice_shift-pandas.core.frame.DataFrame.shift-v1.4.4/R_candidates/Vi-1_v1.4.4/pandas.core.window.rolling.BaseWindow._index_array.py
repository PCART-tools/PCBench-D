    @property
    def _index_array(self):
        # TODO: why do we get here with e.g. MultiIndex?
        if needs_i8_conversion(self._on.dtype):
            return self._on.asi8
        return None
