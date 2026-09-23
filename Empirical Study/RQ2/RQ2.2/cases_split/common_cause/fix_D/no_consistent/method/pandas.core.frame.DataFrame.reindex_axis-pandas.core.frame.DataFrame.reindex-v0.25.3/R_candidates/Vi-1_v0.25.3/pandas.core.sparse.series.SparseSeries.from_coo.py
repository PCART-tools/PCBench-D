    @classmethod
    @Appender(SparseAccessor.from_coo.__doc__)
    def from_coo(cls, A, dense_index=False):
        return _coo_to_sparse_series(A, dense_index=dense_index)
