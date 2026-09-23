    def accumulate(self, binop, initial=no_default):
        """ Repeatedly apply binary function to a sequence, accumulating results.

        This assumes that the bag is ordered.  While this is typically the case
        not all Dask.bag functions preserve this property.

        Examples
        --------
        >>> from operator import add
        >>> b = from_sequence([1, 2, 3, 4, 5], npartitions=2)
        >>> b.accumulate(add).compute()  # doctest: +SKIP
        [1, 3, 6, 10, 15]

        Accumulate also takes an optional argument that will be used as the
        first value.

        >>> b.accumulate(add, initial=-1)  # doctest: +SKIP
        [-1, 0, 2, 5, 9, 14]
        """
        if not _implement_accumulate:
            raise NotImplementedError("accumulate requires `toolz` > 0.7.4"
                                      " or `cytoolz` > 0.7.3.")
        token = tokenize(self, binop, initial)
        binop_name = funcname(binop)
        a = '%s-part-%s' % (binop_name, token)
        b = '%s-first-%s' % (binop_name, token)
        c = '%s-second-%s' % (binop_name, token)
        dsk = {(a, 0): (accumulate_part, binop, (self.name, 0), initial, True),
               (b, 0): (first, (a, 0)),
               (c, 0): (second, (a, 0))}
        for i in range(1, self.npartitions):
            dsk[(a, i)] = (accumulate_part, binop, (self.name, i), (c, i - 1))
            dsk[(b, i)] = (first, (a, i))
            dsk[(c, i)] = (second, (a, i))
        return Bag(merge(self.dask, dsk), b, self.npartitions)
