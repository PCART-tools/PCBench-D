    @Substitution(name='groupby')
    @Appender(_doc_template)
    def mean(self, *args, **kwargs):
        """
        Compute mean of groups, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        nv.validate_groupby_func('mean', args, kwargs, ['numeric_only'])
        try:
            return self._cython_agg_general('mean', **kwargs)
        except GroupByError:
            raise
        except Exception:  # pragma: no cover
            self._set_group_selection()
            f = lambda x: x.mean(axis=self.axis, **kwargs)
            return self._python_agg_general(f)
