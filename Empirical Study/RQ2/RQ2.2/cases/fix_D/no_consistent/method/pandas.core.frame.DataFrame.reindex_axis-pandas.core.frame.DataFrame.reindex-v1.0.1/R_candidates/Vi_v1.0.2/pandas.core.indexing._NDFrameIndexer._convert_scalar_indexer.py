    def _convert_scalar_indexer(self, key, axis: int):
        # if we are accessing via lowered dim, use the last dim
        ax = self.obj._get_axis(min(axis, self.ndim - 1))
        # a scalar
        return ax._convert_scalar_indexer(key, kind=self.name)
