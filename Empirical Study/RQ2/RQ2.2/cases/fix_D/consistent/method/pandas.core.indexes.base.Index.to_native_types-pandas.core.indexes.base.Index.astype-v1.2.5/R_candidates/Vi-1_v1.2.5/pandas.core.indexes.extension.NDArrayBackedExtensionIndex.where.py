    @doc(Index.where)
    def where(self, cond, other=None):
        res_values = self._data.where(cond, other)
        return type(self)._simple_new(res_values, name=self.name)
