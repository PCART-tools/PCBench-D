    def sum(self, split_every=None):
        """ Sum all elements """
        return self.reduction(sum, sum, split_every=split_every)
