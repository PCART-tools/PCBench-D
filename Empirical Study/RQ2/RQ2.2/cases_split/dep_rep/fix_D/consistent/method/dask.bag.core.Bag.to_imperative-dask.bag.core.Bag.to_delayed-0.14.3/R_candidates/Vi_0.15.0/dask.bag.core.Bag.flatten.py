    def flatten(self):
        """ Concatenate nested lists into one long list

        >>> b = from_sequence([[1], [2, 3]])
        >>> list(b)
        [[1], [2, 3]]

        >>> list(b.flatten())
        [1, 2, 3]
        """
        name = 'flatten-' + tokenize(self)
        dsk = dict(((name, i), (list, (toolz.concat, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)
