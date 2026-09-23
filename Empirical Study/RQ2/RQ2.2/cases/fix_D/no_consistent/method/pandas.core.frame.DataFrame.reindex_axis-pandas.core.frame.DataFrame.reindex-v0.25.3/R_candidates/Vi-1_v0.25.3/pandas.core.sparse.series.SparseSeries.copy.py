    def copy(self, deep=True):
        """
        Make a copy of the SparseSeries. Only the actual sparse values need to
        be copied
        """
        # TODO: https://github.com/pandas-dev/pandas/issues/22314
        # We skip the block manager till that is resolved.
        new_data = self.values
        if deep:
            new_data = new_data.copy()
        return self._constructor(
            new_data,
            sparse_index=self.sp_index,
            fill_value=self.fill_value,
            index=self.index.copy(),
            name=self.name,
        ).__finalize__(self)
