    @doc(Index.astype)
    def astype(self, dtype, copy=True):
        res_data = self._data.astype(dtype, copy=copy)
        return Index(res_data, name=self.name)
