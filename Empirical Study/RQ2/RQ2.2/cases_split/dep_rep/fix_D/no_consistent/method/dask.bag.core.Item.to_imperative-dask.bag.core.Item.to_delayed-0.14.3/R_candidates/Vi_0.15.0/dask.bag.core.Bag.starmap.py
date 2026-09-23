    def starmap(self, func, **kwargs):
        """Apply a function using argument tuples from the given bag.

        This is similar to ``itertools.starmap``, except it also accepts
        keyword arguments. In pseudocode, this is could be written as:

        >>> def starmap(func, bag, **kwargs):
        ...     return (func(*args, **kwargs) for args in bag)

        Parameters
        ----------
        func : callable
        **kwargs : Item, Delayed, or object, optional
            Extra keyword arguments to pass to ``func``. These can either be
            normal objects, ``dask.bag.Item``, or ``dask.delayed.Delayed``.

        Examples
        --------
        >>> import dask.bag as db
        >>> data = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
        >>> b = db.from_sequence(data, npartitions=2)

        Apply a function to each argument tuple:

        >>> from operator import add
        >>> b.starmap(add).compute()
        [3, 7, 11, 15, 19]

        Apply a function to each argument tuple, with additional keyword
        arguments:

        >>> def myadd(x, y, z=0):
        ...     return x + y + z
        >>> b.starmap(myadd, z=10).compute()
        [13, 17, 21, 25, 29]

        Keyword arguments can also be instances of ``dask.bag.Item`` or
        ``dask.delayed.Delayed``:

        >>> max_second = b.pluck(1).max()
        >>> max_second.compute()
        10
        >>> b.starmap(myadd, z=max_second).compute()
        [13, 17, 21, 25, 29]
        """
        name = 'starmap-{0}-{1}'.format(funcname(func),
                                        tokenize(self, func, kwargs))
        dsk = self.dask.copy()
        if kwargs:
            kw_dsk, kwargs = unpack_scalar_dask_kwargs(kwargs)
            dsk.update(kw_dsk)
        dsk.update({(name, i): (reify, (starmap_chunk, func, (self.name, i), kwargs))
                   for i in range(self.npartitions)})
        return type(self)(dsk, name, self.npartitions)
