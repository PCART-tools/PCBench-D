    def median(self):
        """
        Compute median of groups, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        try:
            return self._cython_agg_general('median')
        except GroupByError:
            raise
        except Exception:  # pragma: no cover

            def f(x):
                if isinstance(x, np.ndarray):
                    x = Series(x)
                return x.median(axis=self.axis)
            return self._python_agg_general(f)
