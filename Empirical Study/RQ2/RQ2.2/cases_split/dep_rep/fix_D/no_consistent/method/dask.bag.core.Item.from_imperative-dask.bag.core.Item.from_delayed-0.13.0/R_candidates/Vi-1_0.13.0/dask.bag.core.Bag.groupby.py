    def groupby(self, grouper, method=None, npartitions=None, blocksize=2**20,
                max_branch=None):
        """ Group collection by key function

        This requires a full dataset read, serialization and shuffle.
        This is expensive.  If possible you should use ``foldby``.

        Parameters
        ----------
        grouper: function
            Function on which to group elements
        method: str
            Either 'disk' for an on-disk shuffle or 'tasks' to use the task
            scheduling framework.  Use 'disk' if you are on a single machine
            and 'tasks' if you are on a distributed cluster.
        npartitions: int
            If using the disk-based shuffle, the number of output partitions
        blocksize: int
            If using the disk-based shuffle, the size of shuffle blocks
        max_branch: int
            If using the task-based shuffle, the amount of splitting each
            partition undergoes.  Increase this for fewer copies but more
            scheduler overhead.

        Examples
        --------
        >>> b = from_sequence(range(10))
        >>> iseven = lambda x: x % 2 == 0
        >>> dict(b.groupby(iseven))  # doctest: +SKIP
        {True: [0, 2, 4, 6, 8], False: [1, 3, 5, 7, 9]}

        See Also
        --------
        Bag.foldby
        """
        if method is None:
            get = _globals.get('get')
            if (isinstance(get, types.MethodType) and
               'distributed' in get.__func__.__module__):
                method = 'tasks'
            else:
                method = 'disk'
        if method == 'disk':
            return groupby_disk(self, grouper, npartitions=npartitions,
                                blocksize=blocksize)
        elif method == 'tasks':
            return groupby_tasks(self, grouper, max_branch=max_branch)
        else:
            msg = "Shuffle method must be 'disk' or 'tasks'"
            raise NotImplementedError(msg)
