    def map(self, func, *args, **kwargs):
        """Apply a function elementwise across one or more bags.

        Note that all ``Bag`` arguments must be partitioned identically.

        Parameters
        ----------
        func : callable
        *args, **kwargs : Bag, Item, or object
            Extra arguments and keyword arguments to pass to ``func`` *after*
            the calling bag instance. Non-Bag args/kwargs are broadcasted
            across all calls to ``func``.

        Notes
        -----
        For calls with multiple `Bag` arguments, corresponding partitions
        should have the same length; if they do not, the call will error at
        compute time.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5), npartitions=2)
        >>> b2 = db.from_sequence(range(5, 10), npartitions=2)

        Apply a function to all elements in a bag:

        >>> b.map(lambda x: x + 1).compute()
        [1, 2, 3, 4, 5]

        Apply a function with arguments from multiple bags:

        >>> from operator import add
        >>> b.map(add, b2).compute()
        [5, 7, 9, 11, 13]

        Non-bag arguments are broadcast across all calls to the mapped
        function:

        >>> b.map(add, 1).compute()
        [1, 2, 3, 4, 5]

        Keyword arguments are also supported, and have the same semantics as
        regular arguments:

        >>> def myadd(x, y=0):
        ...     return x + y
        >>> b.map(myadd, y=b2).compute()
        [5, 7, 9, 11, 13]
        >>> b.map(myadd, y=1).compute()
        [1, 2, 3, 4, 5]

        Both arguments and keyword arguments can also be instances of
        ``dask.bag.Item``. Here we'll add the max value in the bag to each
        element:

        >>> b.map(myadd, b.max()).compute()
        [4, 5, 6, 7, 8]
        """
        if takes_multiple_arguments(func, varargs=False) and not args:
            warn("Automatic 'splatting' of arguments in `Bag.map` is "
                 "deprecated and will be removed in a future release. "
                 "Please use `Bag.starmap` instead.")
            return self.starmap(func, **kwargs)
        else:
            return bag_map(func, self, *args, **kwargs)
