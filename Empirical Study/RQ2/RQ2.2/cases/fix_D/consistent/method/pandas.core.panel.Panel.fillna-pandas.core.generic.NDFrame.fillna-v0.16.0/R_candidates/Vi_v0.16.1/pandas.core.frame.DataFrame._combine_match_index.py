    def _combine_match_index(self, other, func, level=None, fill_value=None):
        left, right = self.align(other, join='outer', axis=0, level=level, copy=False)
        if fill_value is not None:
            raise NotImplementedError("fill_value %r not supported." %
                                      fill_value)
        return self._constructor(func(left.values.T, right.values).T,
                                 index=left.index,
                                 columns=self.columns, copy=False)
