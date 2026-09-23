    def _compare_constructor(self, other, func):
        if not self._indexed_same(other):
            raise Exception('Can only compare identically-labeled '
                            'same type objects')

        new_data = {}
        for col in self._info_axis:
            new_data[col] = func(self[col], other[col])

        d = self._construct_axes_dict(copy=False)
        return self._constructor(data=new_data, **d)
