    def __str__(self):
        name = self.name if len(self.name) < 10 else self.name[:7] + '...'
        return 'dask.bag<%s, npartitions=%d>' % (name, self.npartitions)
