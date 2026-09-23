    def filter(self, func, dropna=True, *args, **kwargs):  # noqa
        """
        Return a copy of a Series excluding elements from groups that
        do not satisfy the boolean criterion specified by func.

        Parameters
        ----------
        func : function
            To apply to each group. Should return True or False.
        dropna : Drop groups that do not pass the filter. True by default;
            if False, groups that evaluate False are filled with NaNs.

        Examples
        --------
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
        ...                           'foo', 'bar'],
        ...                    'B' : [1, 2, 3, 4, 5, 6],
        ...                    'C' : [2.0, 5., 8., 1., 2., 9.]})
        >>> grouped = df.groupby('A')
        >>> df.groupby('A').B.filter(lambda x: x.mean() > 3.)
        1    2
        3    4
        5    6
        Name: B, dtype: int64

        Returns
        -------
        filtered : Series
        """
        if isinstance(func, compat.string_types):
            wrapper = lambda x: getattr(x, func)(*args, **kwargs)
        else:
            wrapper = lambda x: func(x, *args, **kwargs)

        # Interpret np.nan as False.
        def true_and_notna(x, *args, **kwargs):
            b = wrapper(x, *args, **kwargs)
            return b and notna(b)

        try:
            indices = [self._get_index(name) for name, group in self
                       if true_and_notna(group)]
        except ValueError:
            raise TypeError("the filter must return a boolean result")
        except TypeError:
            raise TypeError("the filter must return a boolean result")

        filtered = self._apply_filter(indices, dropna)
        return filtered
