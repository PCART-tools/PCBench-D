    def cumcount(self, **kwargs):
        """
        Number each item in each group from 0 to the length of that group - 1.

        Essentially this is equivalent to

        >>> self.apply(lambda x: Series(np.arange(len(x)), x.index))

        Parameters
        ----------
        ascending : bool, default True
            If False, number in reverse, from length of group - 1 to 0.

        Example
        -------

        >>> df = pd.DataFrame([['a'], ['a'], ['a'], ['b'], ['b'], ['a']],
        ...                   columns=['A'])
        >>> df
           A
        0  a
        1  a
        2  a
        3  b
        4  b
        5  a
        >>> df.groupby('A').cumcount()
        0    0
        1    1
        2    2
        3    0
        4    1
        5    3
        dtype: int64
        >>> df.groupby('A').cumcount(ascending=False)
        0    3
        1    2
        2    1
        3    1
        4    0
        5    0
        dtype: int64

        """
        self._set_selection_from_grouper()
        ascending = kwargs.pop('ascending', True)

        index = self._selected_obj.index
        cumcounts = self._cumcount_array(ascending=ascending)
        return Series(cumcounts, index)
