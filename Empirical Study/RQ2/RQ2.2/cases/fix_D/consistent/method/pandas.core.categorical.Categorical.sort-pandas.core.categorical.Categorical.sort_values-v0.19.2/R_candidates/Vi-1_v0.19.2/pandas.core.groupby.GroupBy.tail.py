    @Substitution(name='groupby')
    @Appender(_doc_template)
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
        self._reset_group_selection()
        mask = self._cumcount_array(ascending=False) < n
        return self._selected_obj[mask]
