    def _combine_match_columns(self, other, func, level=None):
        assert isinstance(other, Series)
        left, right = self.align(other, join='outer', axis=1, level=level,
                                 copy=False)
        assert left.columns.equals(right.index)
        return ops.dispatch_to_series(left, right, func, axis="columns")
