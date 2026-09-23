    def _set_with_engine(self, key, value):
        values = self._values
        try:
            self.index._engine.set_value(values, key, value)
            return
        except KeyError:
            values[self.index.get_loc(key)] = value
            return
