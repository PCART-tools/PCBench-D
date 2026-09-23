    def min(self, *, axis: int | None = None, skipna: bool = True):
        nv.validate_minmax_axis(axis, self.ndim)

        if not len(self):
            return self._na_value

        mask = self.isna()
        if mask.any():
            if not skipna:
                return self._na_value
            obj = self[~mask]
        else:
            obj = self

        indexer = obj.argsort()[0]
        return obj[indexer]
