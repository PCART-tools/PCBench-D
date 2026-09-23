    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def median(self, **kwargs):
        """
        Compute median of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex

        Returns
        -------
        Series or DataFrame
            Median of values within each group.
        """
        try:
            return self._cython_agg_general(
                "median",
                alt=lambda x, axis: Series(x).median(axis=axis, **kwargs),
                **kwargs
            )
        except GroupByError:
            raise
        except Exception:  # pragma: no cover

            def f(x):
                if isinstance(x, np.ndarray):
                    x = Series(x)
                return x.median(axis=self.axis, **kwargs)

            with _group_selection_context(self):
                return self._python_agg_general(f)
