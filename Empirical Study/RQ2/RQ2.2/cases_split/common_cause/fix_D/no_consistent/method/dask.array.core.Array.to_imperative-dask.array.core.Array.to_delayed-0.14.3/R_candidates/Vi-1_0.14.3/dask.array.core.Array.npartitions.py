    @property
    def npartitions(self):
        return reduce(mul, self.numblocks, 1)
