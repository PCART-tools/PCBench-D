    def __setstate__(self, state):
        self.dask, self.name, self.npartitions = state
