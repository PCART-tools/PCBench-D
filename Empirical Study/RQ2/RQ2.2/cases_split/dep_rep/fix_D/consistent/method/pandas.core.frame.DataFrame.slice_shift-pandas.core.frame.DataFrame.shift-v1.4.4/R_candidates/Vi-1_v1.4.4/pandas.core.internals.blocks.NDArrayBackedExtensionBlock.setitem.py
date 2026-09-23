    def setitem(self, indexer, value):
        if not self._can_hold_element(value):
            return self.coerce_to_target_dtype(value).setitem(indexer, value)

        values = self.values
        if self.ndim > 1:
            # Dont transpose with ndim=1 bc we would fail to invalidate
            #  arr.freq
            values = values.T
        values[indexer] = value
        return self
