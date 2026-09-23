    @property
    def _series(self):
        return {item: Series(self._data.iget(idx), index=self.index, name=item)
                for idx, item in enumerate(self.columns)}
