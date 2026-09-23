    @property
    def series_generator(self):
        return (self.obj._ixs(i, axis=1) for i in range(len(self.columns)))
