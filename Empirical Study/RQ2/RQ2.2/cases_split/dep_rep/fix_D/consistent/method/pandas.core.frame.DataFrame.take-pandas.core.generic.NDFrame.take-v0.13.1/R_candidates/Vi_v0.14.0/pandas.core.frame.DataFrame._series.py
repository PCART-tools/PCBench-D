    @property
    def _series(self):
        result = {}
        for idx, item in enumerate(self.columns):
            result[item] = Series(self._data.iget(idx), index=self.index,
                                  name=item)
        return result
