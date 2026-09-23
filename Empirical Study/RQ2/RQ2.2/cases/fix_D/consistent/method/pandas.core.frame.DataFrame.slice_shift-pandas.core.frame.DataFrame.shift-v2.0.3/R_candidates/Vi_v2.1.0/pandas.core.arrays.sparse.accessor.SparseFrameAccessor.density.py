    @property
    def density(self) -> float:
        """
        Ratio of non-sparse points to total (dense) data points.

        Examples
        --------
        >>> df = pd.DataFrame({"A": pd.arrays.SparseArray([0, 1, 0, 1])})
        >>> df.sparse.density
        0.5
        """
        tmp = np.mean([column.array.density for _, column in self._parent.items()])
        return tmp
