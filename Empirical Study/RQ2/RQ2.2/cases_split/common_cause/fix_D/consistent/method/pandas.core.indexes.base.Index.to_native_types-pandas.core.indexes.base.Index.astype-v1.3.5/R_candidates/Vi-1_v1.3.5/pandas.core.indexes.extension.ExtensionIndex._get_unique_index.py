    def _get_unique_index(self):
        if self.is_unique:
            return self

        result = self._data.unique()
        return type(self)._simple_new(result, name=self.name)
