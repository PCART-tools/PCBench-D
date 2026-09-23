    @property
    def density(self) -> float:
        """
        Ratio of non-sparse points to total (dense) data points.
        """
        tmp = np.mean([column.array.density for _, column in self._parent.items()])
        return tmp
