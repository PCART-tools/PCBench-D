    def min(self, split_every=None):
        """ Minimum element """
        return self.reduction(min, min, split_every=split_every)
