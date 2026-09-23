    @classmethod
    def from_array(cls, arr, index=None, name=None, dtype=None, copy=False,
                   fastpath=False):
        # return a sparse series here
        if isinstance(arr, ABCSparseArray):
            from pandas.sparse.series import SparseSeries
            cls = SparseSeries

        return cls(arr, index=index, name=name, dtype=dtype, copy=copy, fastpath=fastpath)
