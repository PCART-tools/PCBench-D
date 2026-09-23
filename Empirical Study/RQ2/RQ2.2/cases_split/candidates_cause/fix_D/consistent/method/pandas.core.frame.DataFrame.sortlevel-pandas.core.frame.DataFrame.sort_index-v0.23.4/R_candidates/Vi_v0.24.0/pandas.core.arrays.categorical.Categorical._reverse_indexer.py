    def _reverse_indexer(self):
        """
        Compute the inverse of a categorical, returning
        a dict of categories -> indexers.

        *This is an internal function*

        Returns
        -------
        dict of categories -> indexers

        Example
        -------
        In [1]: c = pd.Categorical(list('aabca'))

        In [2]: c
        Out[2]:
        [a, a, b, c, a]
        Categories (3, object): [a, b, c]

        In [3]: c.categories
        Out[3]: Index([u'a', u'b', u'c'], dtype='object')

        In [4]: c.codes
        Out[4]: array([0, 0, 1, 2, 0], dtype=int8)

        In [5]: c._reverse_indexer()
        Out[5]: {'a': array([0, 1, 4]), 'b': array([2]), 'c': array([3])}

        """
        categories = self.categories
        r, counts = libalgos.groupsort_indexer(self.codes.astype('int64'),
                                               categories.size)
        counts = counts.cumsum()
        result = [r[counts[indexer]:counts[indexer + 1]]
                  for indexer in range(len(counts) - 1)]
        result = dict(zip(categories, result))
        return result
