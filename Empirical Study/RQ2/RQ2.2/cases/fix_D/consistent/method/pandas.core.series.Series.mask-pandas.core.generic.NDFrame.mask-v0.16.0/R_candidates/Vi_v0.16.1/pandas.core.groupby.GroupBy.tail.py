    def tail(self, n=5):
        """
        Returns last n rows of each group

        Essentially equivalent to ``.apply(lambda x: x.tail(n))``,
        except ignores as_index flag.

        Examples
        --------

        >>> df = DataFrame([['a', 1], ['a', 2], ['b', 1], ['b', 2]],
                            columns=['A', 'B'])
        >>> df.groupby('A').tail(1)
           A  B
        1  a  2
        3  b  2
        >>> df.groupby('A').head(1)
           A  B
        0  a  1
        2  b  1

        """
        obj = self._selected_obj
        rng = np.arange(0, -self.grouper._max_groupsize, -1, dtype='int64')
        in_tail = self._cumcount_array(rng, ascending=False) > -n
        tail = obj[in_tail]
        return tail
