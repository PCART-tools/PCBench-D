    @doc(Index._shallow_copy)
    def _shallow_copy(self, values, name: Hashable = no_default):
        name = self.name if name is no_default else name

        if values.dtype.kind == "f":
            return Index(values, name=name, dtype=np.float64)
        # GH 46675 & 43885: If values is equally spaced, return a
        # more memory-compact RangeIndex instead of Index with 64-bit dtype
        unique_diffs = unique_deltas(values)
        if len(unique_diffs) == 1 and unique_diffs[0] != 0:
            diff = unique_diffs[0]
            new_range = range(values[0], values[-1] + diff, diff)
            return type(self)._simple_new(new_range, name=name)
        else:
            return self._constructor._simple_new(values, name=name)
