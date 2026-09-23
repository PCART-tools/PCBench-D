    @classmethod
    def from_array(cls, arr, index=None, name=None, copy=False,
                   fill_value=None, fastpath=False):
        """Construct SparseSeries from array.

        .. deprecated:: 0.23.0
            Use the pd.SparseSeries(..) constructor instead.
        """
        warnings.warn("'from_array' is deprecated and will be removed in a "
                      "future version. Please use the pd.SparseSeries(..) "
                      "constructor instead.", FutureWarning, stacklevel=2)
        return cls(arr, index=index, name=name, copy=copy,
                   fill_value=fill_value, fastpath=fastpath)
