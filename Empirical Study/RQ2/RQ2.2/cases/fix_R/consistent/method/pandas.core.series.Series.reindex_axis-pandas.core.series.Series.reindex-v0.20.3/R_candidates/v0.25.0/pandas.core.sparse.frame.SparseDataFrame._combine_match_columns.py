    def _combine_match_columns(self, other, func, level=None):
        # patched version of DataFrame._combine_match_columns to account for
        # NumPy circumventing __rsub__ with float64 types, e.g.: 3.0 - series,
        # where 3.0 is numpy.float64 and series is a SparseSeries. Still
        # possible for this to happen, which is bothersome

        if level is not None:
            raise NotImplementedError("'level' argument is not supported")

        left, right = self.align(other, join="outer", axis=1, level=level, copy=False)
        assert left.columns.equals(right.index)

        new_data = {}

        for col in left.columns:
            new_data[col] = func(left[col], float(right[col]))

        return self._constructor(
            new_data,
            index=left.index,
            columns=left.columns,
            default_fill_value=self.default_fill_value,
        ).__finalize__(self)
