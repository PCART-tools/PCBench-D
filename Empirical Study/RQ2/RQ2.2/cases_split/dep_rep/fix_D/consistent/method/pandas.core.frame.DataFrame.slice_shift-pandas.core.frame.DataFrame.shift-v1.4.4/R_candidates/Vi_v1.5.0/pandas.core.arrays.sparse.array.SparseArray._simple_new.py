    @classmethod
    def _simple_new(
        cls: type[SparseArrayT],
        sparse_array: np.ndarray,
        sparse_index: SparseIndex,
        dtype: SparseDtype,
    ) -> SparseArrayT:
        new = object.__new__(cls)
        new._sparse_index = sparse_index
        new._sparse_values = sparse_array
        new._dtype = dtype
        return new
