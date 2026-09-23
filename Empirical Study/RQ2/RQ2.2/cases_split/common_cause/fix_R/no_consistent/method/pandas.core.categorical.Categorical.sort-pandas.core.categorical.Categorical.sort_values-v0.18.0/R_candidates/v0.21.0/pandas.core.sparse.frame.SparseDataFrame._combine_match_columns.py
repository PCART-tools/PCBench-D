    def _combine_match_columns(self, other, func, level=None, fill_value=None,
                               try_cast=True):
        # patched version of DataFrame._combine_match_columns to account for
        # NumPy circumventing __rsub__ with float64 types, e.g.: 3.0 - series,
        # where 3.0 is numpy.float64 and series is a SparseSeries. Still
        # possible for this to happen, which is bothersome

        if fill_value is not None:
            raise NotImplementedError("'fill_value' argument is not supported")
        if level is not None:
            raise NotImplementedError("'level' argument is not supported")

        new_data = {}

        union = intersection = self.columns

        if not union.equals(other.index):
            union = other.index.union(self.columns)
            intersection = other.index.intersection(self.columns)

        for col in intersection:
            new_data[col] = func(self[col], float(other[col]))

        return self._constructor(
            new_data, index=self.index, columns=union,
            default_fill_value=self.default_fill_value).__finalize__(self)
