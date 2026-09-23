    def concat(self):
        """ Concatenate nested lists into one long list

        >>> b = from_sequence([[1], [2, 3]])
        >>> list(b)
        [[1], [2, 3]]

        >>> list(b.concat())
        [1, 2, 3]
        """
        name = 'concat-' + tokenize(self)
        dsk = dict(((name, i), (list, (toolz.concat, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)
