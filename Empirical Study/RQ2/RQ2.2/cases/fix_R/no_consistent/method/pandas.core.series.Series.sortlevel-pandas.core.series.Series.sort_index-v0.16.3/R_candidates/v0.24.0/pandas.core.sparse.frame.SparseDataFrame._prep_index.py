    def _prep_index(self, data, index, columns):
        N, K = data.shape
        if index is None:
            index = ibase.default_index(N)
        if columns is None:
            columns = ibase.default_index(K)

        if len(columns) != K:
            raise ValueError('Column length mismatch: {columns} vs. {K}'
                             .format(columns=len(columns), K=K))
        if len(index) != N:
            raise ValueError('Index length mismatch: {index} vs. {N}'
                             .format(index=len(index), N=N))
        return index, columns
