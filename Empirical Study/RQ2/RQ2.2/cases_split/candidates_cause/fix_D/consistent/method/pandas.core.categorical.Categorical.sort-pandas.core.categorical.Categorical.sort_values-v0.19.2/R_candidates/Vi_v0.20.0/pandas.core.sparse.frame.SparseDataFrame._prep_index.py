    def _prep_index(self, data, index, columns):
        N, K = data.shape
        if index is None:
            index = _default_index(N)
        if columns is None:
            columns = _default_index(K)

        if len(columns) != K:
            raise ValueError('Column length mismatch: %d vs. %d' %
                             (len(columns), K))
        if len(index) != N:
            raise ValueError('Index length mismatch: %d vs. %d' %
                             (len(index), N))
        return index, columns
