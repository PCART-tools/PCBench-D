    def _set_with_engine(self, key, value):
        values = self.values
        try:
            self.index._engine.set_value(values, key, value)
            self._check_setitem_copy()
            return
        except KeyError:
            values[self.index.get_loc(key)] = value
            return
