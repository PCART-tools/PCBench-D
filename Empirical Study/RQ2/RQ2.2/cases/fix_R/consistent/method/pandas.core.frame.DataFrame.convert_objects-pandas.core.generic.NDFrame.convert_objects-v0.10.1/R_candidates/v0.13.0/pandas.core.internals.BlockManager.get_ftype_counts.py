    def get_ftype_counts(self):
        """ return a dict of the counts of dtypes in BlockManager """
        self._consolidate_inplace()
        counts = dict()
        for b in self.blocks:
            counts[b.ftype] = counts.get(b.ftype, 0) + b.shape[0]
        return counts
