    @staticmethod
    def _prep_index(data, index, columns):
        import pandas.core.indexes.base as ibase

        N, K = data.shape
        if index is None:
            index = ibase.default_index(N)
        if columns is None:
            columns = ibase.default_index(K)

        if len(columns) != K:
            raise ValueError(f"Column length mismatch: {len(columns)} vs. {K}")
        if len(index) != N:
            raise ValueError(f"Index length mismatch: {len(index)} vs. {N}")
        return index, columns
