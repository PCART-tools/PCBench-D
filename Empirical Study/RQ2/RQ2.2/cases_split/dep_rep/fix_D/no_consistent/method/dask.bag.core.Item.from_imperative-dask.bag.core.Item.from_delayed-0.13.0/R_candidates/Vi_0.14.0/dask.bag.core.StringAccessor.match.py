    def match(self, pattern):
        """ Filter strings by those that match a pattern

        Examples
        --------

        >>> import dask.bag as db
        >>> b = db.from_sequence(['Alice Smith', 'Bob Jones', 'Charlie Smith'])
        >>> list(b.str.match('*Smith'))
        ['Alice Smith', 'Charlie Smith']

        See Also
        --------
        fnmatch.fnmatch
        """
        from fnmatch import fnmatch
        return self._bag.filter(partial(fnmatch, pat=pattern))
