    @classmethod
    def _simple_new(cls, sparse_array, sparse_index, dtype):
        # type: (np.ndarray, SparseIndex, SparseDtype) -> 'SparseArray'
        new = cls([])
        new._sparse_index = sparse_index
        new._sparse_values = sparse_array
        new._dtype = dtype
        return new
