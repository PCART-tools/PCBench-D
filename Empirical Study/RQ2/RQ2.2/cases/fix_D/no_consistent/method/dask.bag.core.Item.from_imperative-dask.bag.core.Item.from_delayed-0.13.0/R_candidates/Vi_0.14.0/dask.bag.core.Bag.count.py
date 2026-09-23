    def count(self, split_every=None):
        """ Count the number of elements """
        return self.reduction(count, sum, split_every=split_every)
