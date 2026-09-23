    def _wrap_result(self, result, **kwargs):

        # leave as it is to keep extract and get_dummies results
        # can be merged to _wrap_result_expand in v0.17
        from pandas.core.series import Series
        from pandas.core.frame import DataFrame
        from pandas.core.index import Index

        if not hasattr(result, 'ndim'):
            return result
        name = kwargs.get('name') or getattr(result, 'name', None) or self.series.name

        if result.ndim == 1:
            if isinstance(self.series, Index):
                # if result is a boolean np.array, return the np.array
                # instead of wrapping it into a boolean Index (GH 8875)
                if is_bool_dtype(result):
                    return result
                return Index(result, name=name)
            return Series(result, index=self.series.index, name=name)
        else:
            assert result.ndim < 3
            return DataFrame(result, index=self.series.index)
