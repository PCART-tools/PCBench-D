    def head(self, n=5):
        """
        Returns first n rows of each group.

        Essentially equivalent to ``.apply(lambda x: x.head(n))``

        Example
        -------

        >>> df = DataFrame([[1, 2], [1, 4], [5, 6]],
                            columns=['A', 'B'])
        >>> df.groupby('A', as_index=False).head(1)
           A  B
        0  1  2
        2  5  6
        >>> df.groupby('A').head(1)
             A  B
        A
        1 0  1  2
        5 2  5  6

        """
        rng = np.arange(self.grouper._max_groupsize, dtype='int64')
        in_head = self._cumcount_array(rng) < n
        head = self.obj[in_head]
        if self.as_index:
            head.index = self._index_with_as_index(in_head)
        return head
