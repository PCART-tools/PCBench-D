    def _combine_match_index(self, other, func, level=None):
        left, right = self.align(other, join='outer', axis=0, level=level,
                                 copy=False)
        assert left.index.equals(right.index)

        if left._is_mixed_type or right._is_mixed_type:
            # operate column-wise; avoid costly object-casting in `.values`
            return ops.dispatch_to_series(left, right, func)
        else:
            # fastpath --> operate directly on values
            with np.errstate(all="ignore"):
                new_data = func(left.values.T, right.values).T
            return self._constructor(new_data,
                                     index=left.index, columns=self.columns,
                                     copy=False)
