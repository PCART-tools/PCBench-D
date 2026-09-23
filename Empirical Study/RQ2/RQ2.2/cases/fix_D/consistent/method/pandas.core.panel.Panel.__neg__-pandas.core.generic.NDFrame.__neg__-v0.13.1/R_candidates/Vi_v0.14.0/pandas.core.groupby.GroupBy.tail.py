    def tail(self, n=5):
        """
        Returns last n rows of each group

        Essentially equivalent to ``.apply(lambda x: x.tail(n))``,
        except ignores as_index flag.

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
        0  1  2
        2  5  6

        """
        obj = self._selected_obj
        rng = np.arange(0, -self.grouper._max_groupsize, -1, dtype='int64')
        in_tail = self._cumcount_array(rng, ascending=False) > -n
        tail = obj[in_tail]
        return tail
