    def take(self, k, npartitions=1, compute=True):
        """ Take the first k elements

        Parameters
        ----------
        k : int
            The number of elements to return
        npartitions : int, optional
            Elements are only taken from the first ``npartitions``, with a
            default of 1. If there are fewer than ``k`` rows in the first
            ``npartitions`` a warning will be raised and any found rows
            returned. Pass -1 to use all partitions.
        compute : bool, optional
            Whether to compute the result, default is True.

        >>> b = from_sequence(range(10))
        >>> b.take(3)  # doctest: +SKIP
        (0, 1, 2)
        """

        if npartitions <= -1:
            npartitions = self.npartitions
        if npartitions > self.npartitions:
            raise ValueError("only {} partitions, take "
                             "received {}".format(self.npartitions, npartitions))

        token = tokenize(self, k, npartitions)
        name = 'take-' + token

        if npartitions > 1:
            name_p = 'take-partial-' + token

            dsk = {}
            for i in range(npartitions):
                dsk[(name_p, i)] = (list, (take, k, (self.name, i)))

            concat = (toolz.concat, ([(name_p, i) for i in range(npartitions)]))
            dsk[(name, 0)] = (safe_take, k, concat)
        else:
            dsk = {(name, 0): (safe_take, k, (self.name, 0))}

        b = Bag(merge(self.dask, dsk), name, 1)

        if compute:
            return tuple(b.compute())
        else:
            return b
