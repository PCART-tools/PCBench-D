    def any(self, split_every=None):
        """ Are any of the elements truthy? """
        return self.reduction(any, any, split_every=split_every)
