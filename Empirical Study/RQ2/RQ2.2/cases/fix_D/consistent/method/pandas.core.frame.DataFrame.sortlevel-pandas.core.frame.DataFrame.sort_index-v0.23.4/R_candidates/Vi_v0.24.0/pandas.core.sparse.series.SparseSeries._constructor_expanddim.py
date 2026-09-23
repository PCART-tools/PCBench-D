    @property
    def _constructor_expanddim(self):
        from pandas.core.sparse.api import SparseDataFrame
        return SparseDataFrame
