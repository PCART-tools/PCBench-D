    @Substitution(name='groupby', see_also=_common_see_also)
    def head(self, n=5):
        """
        Returns first n rows of each group.

        Essentially equivalent to ``.apply(lambda x: x.head(n))``,
        except ignores as_index flag.

        %(see_also)s

        Examples
        --------

        >>> df = pd.DataFrame([[1, 2], [1, 4], [5, 6]],
                              columns=['A', 'B'])
        >>> df.groupby('A', as_index=False).head(1)
           A  B
        0  1  2
        2  5  6
        >>> df.groupby('A').head(1)
           A  B
        0  1  2
        2  5  6
        """
        self._reset_group_selection()
        mask = self._cumcount_array() < n
        return self._selected_obj[mask]
