    def apply(self, func):
        name = 'apply-{0}-{1}'.format(funcname(func), tokenize(self, func))
        dsk = {name: (func, self.key)}
        return Item(merge(self.dask, dsk), name)
