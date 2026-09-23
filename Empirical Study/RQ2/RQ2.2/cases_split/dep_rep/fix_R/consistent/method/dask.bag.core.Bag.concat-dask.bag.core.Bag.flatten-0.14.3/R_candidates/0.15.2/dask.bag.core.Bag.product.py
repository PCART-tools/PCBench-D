    def product(self, other):
        """ Cartesian product between two bags """
        assert isinstance(other, Bag)
        name = 'product-' + tokenize(self, other)
        n, m = self.npartitions, other.npartitions
        dsk = dict(((name, i * m + j),
                   (list, (itertools.product, (self.name, i),
                                              (other.name, j))))
                   for i in range(n) for j in range(m))
        return type(self)(merge(self.dask, other.dask, dsk), name, n * m)
