    def _combine_match_index(self, other, func, level=None):
        left, right = self.align(other, join='outer', axis=0, level=level,
                                 copy=False)
        new_data = func(left.values.T, right.values).T
        return self._constructor(new_data,
                                 index=left.index, columns=self.columns,
                                 copy=False)
