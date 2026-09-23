    def map(self, func, **kwargs):
        """ Map a function across all elements in collection

        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5))
        >>> list(b.map(lambda x: x * 10))  # doctest: +SKIP
        [0, 10, 20, 30, 40]

        Keyword arguments are passed through to ``func``. These can be either
        ``dask.bag.Item``, or normal python objects.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(1, 101), npartitions=10)
        >>> def div(num, den=1):
        ...     return num / den

        Using a python object:

        >>> hi = b.max().compute()
        >>> hi
        100
        >>> b.map(div, den=hi).take(5)
        (0.01, 0.02, 0.03, 0.04, 0.05)

        Using an ``Item``:

        >>> b.map(div, den=b.max()).take(5)
        (0.01, 0.02, 0.03, 0.04, 0.05)

        Note that while both versions give the same output, the second forms a
        single graph, and then computes everything at once, and in some cases
        may be more efficient.
        """
        name = 'map-{0}-{1}'.format(funcname(func),
                                    tokenize(self, func, kwargs))
        if takes_multiple_arguments(func):
            func = partial(apply, func)
        dsk = self.dask.copy()
        if kwargs:
            kw_dsk, kw_pairs = unpack_kwargs(kwargs)
            dsk.update(kw_dsk)
            func = (apply, partial, [func], (dict, kw_pairs))
        dsk.update(((name, i), (reify, (map, func, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(dsk, name, self.npartitions)
