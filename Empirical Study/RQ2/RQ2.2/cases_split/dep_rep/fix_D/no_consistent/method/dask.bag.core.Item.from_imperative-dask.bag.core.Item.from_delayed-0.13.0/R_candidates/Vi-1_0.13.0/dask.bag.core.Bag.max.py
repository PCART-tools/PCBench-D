    def max(self, split_every=None):
        """ Maximum element """
        return self.reduction(max, max, split_every=split_every)
