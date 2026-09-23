    def map_partitions(self, func, *args, **kwargs):
        """Apply a function to every partition across one or more bags.

        Note that all ``Bag`` arguments must be partitioned identically.

        Parameters
        ----------
        func : callable
        *args, **kwargs : Bag, Item, Delayed, or object
            Arguments and keyword arguments to pass to ``func``.
            Partitions from this bag will be the first argument, and these will
            be passed *after*.

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
        return map_partitions(func, self, *args, **kwargs)
