    def _combine_match_columns(self, other, func, level=None, try_cast=True):
        left, right = self.align(other, join='outer', axis=1, level=level,
                                 copy=False)

        new_data = left._data.eval(func=func, other=right,
                                   axes=[left.columns, self.index],
                                   try_cast=try_cast)
        return self._constructor(new_data)
