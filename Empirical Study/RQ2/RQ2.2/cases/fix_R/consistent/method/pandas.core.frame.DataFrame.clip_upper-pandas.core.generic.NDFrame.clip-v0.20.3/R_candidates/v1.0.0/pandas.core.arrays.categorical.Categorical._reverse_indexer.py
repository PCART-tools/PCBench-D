    def _reverse_indexer(self) -> Dict[Hashable, np.ndarray]:
        """
        Compute the inverse of a categorical, returning
        a dict of categories -> indexers.

        *This is an internal function*

        Returns
        -------
        dict of categories -> indexers

        Examples
        --------
        >>> c = pd.Categorical(list('aabca'))
        >>> c
        [a, a, b, c, a]
        Categories (3, object): [a, b, c]
        >>> c.categories
        Index(['a', 'b', 'c'], dtype='object')
        >>> c.codes
        array([0, 0, 1, 2, 0], dtype=int8)
        >>> c._reverse_indexer()
        {'a': array([0, 1, 4]), 'b': array([2]), 'c': array([3])}

        """
        categories = self.categories
        r, counts = libalgos.groupsort_indexer(
            self.codes.astype("int64"), categories.size
        )
        counts = counts.cumsum()
        _result = (r[start:end] for start, end in zip(counts, counts[1:]))
        result = dict(zip(categories, _result))
        return result
