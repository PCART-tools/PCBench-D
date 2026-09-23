    @property
    def size(self):
        """ Number of elements in array """
        return reduce(mul, self.shape, 1)
