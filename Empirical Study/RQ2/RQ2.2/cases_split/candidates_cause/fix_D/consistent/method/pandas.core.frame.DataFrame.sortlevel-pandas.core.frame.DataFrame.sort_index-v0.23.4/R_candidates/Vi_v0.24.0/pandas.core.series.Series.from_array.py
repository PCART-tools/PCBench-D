    @classmethod
    def from_array(cls, arr, index=None, name=None, dtype=None, copy=False,
                   fastpath=False):
        """
        Construct Series from array.

        .. deprecated :: 0.23.0
            Use pd.Series(..) constructor instead.
        """
        warnings.warn("'from_array' is deprecated and will be removed in a "
                      "future version. Please use the pd.Series(..) "
                      "constructor instead.", FutureWarning, stacklevel=2)
        if isinstance(arr, ABCSparseArray):
            from pandas.core.sparse.series import SparseSeries
            cls = SparseSeries
        return cls(arr, index=index, name=name, dtype=dtype,
                   copy=copy, fastpath=fastpath)
