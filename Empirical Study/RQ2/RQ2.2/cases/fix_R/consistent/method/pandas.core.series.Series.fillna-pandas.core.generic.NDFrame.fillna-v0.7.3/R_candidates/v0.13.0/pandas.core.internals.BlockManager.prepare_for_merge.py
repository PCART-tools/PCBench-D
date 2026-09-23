    def prepare_for_merge(self, *args, **kwargs):
        """ prepare for merging, return a new block manager with
        Sparse -> Dense
        """
        self._consolidate_inplace()
        if self._has_sparse:
            return self.apply('prepare_for_merge', *args, **kwargs)
        return self
