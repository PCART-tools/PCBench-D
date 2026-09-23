    def filter(self, predicate):
        """ Filter elements in collection by a predicate function

        >>> def iseven(x):
        ...     return x % 2 == 0

        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5))
        >>> list(b.filter(iseven))  # doctest: +SKIP
        [0, 2, 4]
        """
        name = 'filter-{0}-{1}'.format(funcname(predicate),
                                       tokenize(self, predicate))
        dsk = dict(((name, i), (reify, (filter, predicate, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)
