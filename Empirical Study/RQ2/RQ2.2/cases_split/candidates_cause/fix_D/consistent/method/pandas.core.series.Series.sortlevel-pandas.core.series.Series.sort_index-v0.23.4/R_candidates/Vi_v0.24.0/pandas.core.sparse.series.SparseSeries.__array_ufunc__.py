    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # avoid infinite recursion for other SparseSeries inputs
        inputs = tuple(
            x.values if isinstance(x, type(self)) else x
            for x in inputs
        )
        result = self.values.__array_ufunc__(ufunc, method, *inputs, **kwargs)
        return self._constructor(result, index=self.index,
                                 sparse_index=self.sp_index,
                                 fill_value=result.fill_value,
                                 copy=False).__finalize__(self)
