    def nunique(self, dropna: bool = True):
        """
        Return DataFrame with number of distinct observations per group for
        each column.

        Parameters
        ----------
        dropna : bool, default True
            Don't include NaN in the counts.

        Returns
        -------
        nunique: DataFrame

        Examples
        --------
        >>> df = pd.DataFrame({'id': ['spam', 'egg', 'egg', 'spam',
        ...                           'ham', 'ham'],
        ...                    'value1': [1, 5, 5, 2, 5, 5],
        ...                    'value2': list('abbaxy')})
        >>> df
             id  value1 value2
        0  spam       1      a
        1   egg       5      b
        2   egg       5      b
        3  spam       2      a
        4   ham       5      x
        5   ham       5      y

        >>> df.groupby('id').nunique()
            id  value1  value2
        id
        egg    1       1       1
        ham    1       1       2
        spam   1       2       1

        Check for rows with the same id but conflicting values:

        >>> df.groupby('id').filter(lambda g: (g.nunique() > 1).any())
             id  value1 value2
        0  spam       1      a
        3  spam       2      a
        4   ham       5      x
        5   ham       5      y
        """

        obj = self._selected_obj

        def groupby_series(obj, col=None):
            return SeriesGroupBy(obj, selection=col, grouper=self.grouper).nunique(
                dropna=dropna
            )

        if isinstance(obj, Series):
            results = groupby_series(obj)
        else:
            # TODO: this is duplicative of how GroupBy naturally works
            # Try to consolidate with normal wrapping functions
            from pandas.core.reshape.concat import concat

            axis_number = obj._get_axis_number(self.axis)
            other_axis = int(not axis_number)
            if axis_number == 0:
                iter_func = obj.items
            else:
                iter_func = obj.iterrows

            results = [groupby_series(content, label) for label, content in iter_func()]
            results = concat(results, axis=1)

            if axis_number == 1:
                results = results.T

            results._get_axis(other_axis).names = obj._get_axis(other_axis).names

        if not self.as_index:
            results.index = ibase.default_index(len(results))
        return results
