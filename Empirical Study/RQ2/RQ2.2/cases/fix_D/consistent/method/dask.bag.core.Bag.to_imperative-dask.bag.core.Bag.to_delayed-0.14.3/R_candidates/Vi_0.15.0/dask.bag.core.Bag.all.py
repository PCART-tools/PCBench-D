    def all(self, split_every=None):
        """ Are all elements truthy? """
        return self.reduction(all, all, split_every=split_every)
