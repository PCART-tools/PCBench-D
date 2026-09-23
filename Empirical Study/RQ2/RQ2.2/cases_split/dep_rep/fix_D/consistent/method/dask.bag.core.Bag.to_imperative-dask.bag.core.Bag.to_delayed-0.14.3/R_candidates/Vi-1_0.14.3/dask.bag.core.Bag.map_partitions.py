    def map_partitions(self, func, **kwargs):
        """ Apply function to every partition within collection

        Note that this requires you to understand how dask.bag partitions your
        data and so is somewhat internal.

        >>> b.map_partitions(myfunc)  # doctest: +SKIP

        Keyword arguments are passed through to ``func``. These can be either
        ``dask.bag.Item``, or normal python objects.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(1, 101), npartitions=10)
        >>> def div(nums, den=1):
        ...     return [num / den for num in nums]

        Using a python object:

        >>> hi = b.max().compute()
        >>> hi
        100
        >>> b.map_partitions(div, den=hi).take(5)
        (0.01, 0.02, 0.03, 0.04, 0.05)

        Using an ``Item``:

        >>> b.map_partitions(div, den=b.max()).take(5)
        (0.01, 0.02, 0.03, 0.04, 0.05)

        Note that while both versions give the same output, the second forms a
        single graph, and then computes everything at once, and in some cases
        may be more efficient.
        """
        name = 'map-partitions-{0}-{1}'.format(funcname(func),
                                               tokenize(self, func, kwargs))
        dsk = self.dask.copy()
        if kwargs:
            kw_dsk, kw_pairs = unpack_kwargs(kwargs)
            dsk.update(kw_dsk)
        dsk.update(((name, i),
                    (apply, func, [(self.name, i)], (dict, kw_pairs))
                    if kwargs else (func, (self.name, i)))
                   for i in range(self.npartitions))
        return type(self)(dsk, name, self.npartitions)
