    @doc(Index.fillna)
    def fillna(self, value, downcast=None):
        value = self._require_scalar(value)
        cat = self._data.fillna(value)
        return type(self)._simple_new(cat, name=self.name)
