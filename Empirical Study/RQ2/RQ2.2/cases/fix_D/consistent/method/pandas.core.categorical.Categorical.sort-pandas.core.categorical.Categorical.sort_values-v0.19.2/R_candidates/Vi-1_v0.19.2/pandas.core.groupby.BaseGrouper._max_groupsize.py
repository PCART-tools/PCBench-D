    @cache_readonly
    def _max_groupsize(self):
        """
        Compute size of largest group
        """
        # For many items in each group this is much faster than
        # self.size().max(), in worst case marginally slower
        if self.indices:
            return max(len(v) for v in self.indices.values())
        else:
            return 0
