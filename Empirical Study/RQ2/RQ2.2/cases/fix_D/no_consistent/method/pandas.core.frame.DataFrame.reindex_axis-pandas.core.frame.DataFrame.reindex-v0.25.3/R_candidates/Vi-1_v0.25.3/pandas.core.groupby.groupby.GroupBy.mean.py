    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def mean(self, *args, **kwargs):
        """
        Compute mean of groups, excluding missing values.

        Returns
        -------
        pandas.Series or pandas.DataFrame
        %(see_also)s
        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 1, 2, 1, 2],
        ...                    'B': [np.nan, 2, 3, 4, 5],
        ...                    'C': [1, 2, 1, 1, 2]}, columns=['A', 'B', 'C'])

        Groupby one column and return the mean of the remaining columns in
        each group.

        >>> df.groupby('A').mean()
             B         C
        A
        1  3.0  1.333333
        2  4.0  1.500000

        Groupby two columns and return the mean of the remaining column.

        >>> df.groupby(['A', 'B']).mean()
               C
        A B
        1 2.0  2
          4.0  1
        2 3.0  1
          5.0  2

        Groupby one column and return the mean of only particular column in
        the group.

        >>> df.groupby('A')['B'].mean()
        A
        1    3.0
        2    4.0
        Name: B, dtype: float64
        """
        nv.validate_groupby_func("mean", args, kwargs, ["numeric_only"])
        try:
            return self._cython_agg_general(
                "mean", alt=lambda x, axis: Series(x).mean(**kwargs), **kwargs
            )
        except GroupByError:
            raise
        except Exception:  # pragma: no cover
            with _group_selection_context(self):
                f = lambda x: x.mean(axis=self.axis, **kwargs)
                return self._python_agg_general(f)
