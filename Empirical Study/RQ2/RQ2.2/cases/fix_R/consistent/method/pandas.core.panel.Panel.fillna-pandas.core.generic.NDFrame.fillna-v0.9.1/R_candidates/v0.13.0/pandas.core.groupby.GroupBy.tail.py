    def tail(self, n=5):
        """
        Returns last n rows of each group

        Essentially equivalent to ``.apply(lambda x: x.tail(n))``

        Example
        -------

        >>> df = DataFrame([[1, 2], [1, 4], [5, 6]],
                            columns=['A', 'B'])
        >>> df.groupby('A', as_index=False).tail(1)
           A  B
        0  1  2
        2  5  6
        >>> df.groupby('A').head(1)
             A  B
        A
        1 0  1  2
        5 2  5  6

        """
        rng = np.arange(0, -self.grouper._max_groupsize, -1, dtype='int64')
        in_tail = self._cumcount_array(rng, ascending=False) > -n
        tail = self.obj[in_tail]
        if self.as_index:
            tail.index = self._index_with_as_index(in_tail)
        return tail
