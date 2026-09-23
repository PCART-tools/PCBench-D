    def get_dtype_counts(self):
        """ return a dict of the counts of dtypes in BlockManager """
        self._consolidate_inplace()
        counts = dict()
        for b in self.blocks:
            counts[b.dtype.name] = counts.get(b.dtype.name, 0) + b.shape[0]
        return counts
