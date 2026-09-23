    def _combine_match_columns(self, other, func, level=None, fill_value=None):
        left, right = self.align(other, join='outer', axis=1, level=level,
                                 copy=False)
        if fill_value is not None:
            raise NotImplementedError("fill_value %r not supported" %
                                      fill_value)

        new_data = left._data.eval(func=func, other=right,
                                   axes=[left.columns, self.index])
        return self._constructor(new_data)
