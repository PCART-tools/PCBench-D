    def size(self):
        """
        Compute group sizes

        """
        index = self.result_index
        base = Series(np.zeros(len(index), dtype=np.int64), index=index)
        indices = self.indices
        for k, v in compat.iteritems(indices):
            indices[k] = len(v)
        bin_counts = Series(indices, dtype=np.int64)
        # make bin_counts.index to have same name to preserve it
        bin_counts.index.name = index.name
        result = base.add(bin_counts, fill_value=0)
        # addition with fill_value changes dtype to float64
        result = result.astype(np.int64)
        return result
