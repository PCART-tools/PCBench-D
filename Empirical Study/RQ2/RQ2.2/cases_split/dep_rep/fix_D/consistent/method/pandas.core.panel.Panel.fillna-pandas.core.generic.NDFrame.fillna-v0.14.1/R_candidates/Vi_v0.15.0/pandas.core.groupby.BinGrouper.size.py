    def size(self):
        """
        Compute group sizes

        """
        base = Series(np.zeros(len(self.result_index), dtype=np.int64),
                      index=self.result_index)
        indices = self.indices
        for k, v in compat.iteritems(indices):
            indices[k] = len(v)
        bin_counts = Series(indices, dtype=np.int64)
        result = base.add(bin_counts, fill_value=0)
        # addition with fill_value changes dtype to float64
        result = result.astype(np.int64)
        return result
