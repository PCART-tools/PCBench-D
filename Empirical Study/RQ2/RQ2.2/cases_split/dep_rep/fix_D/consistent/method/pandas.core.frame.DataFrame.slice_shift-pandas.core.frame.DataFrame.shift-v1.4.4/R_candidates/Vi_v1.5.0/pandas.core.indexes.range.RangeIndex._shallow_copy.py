    @doc(Int64Index._shallow_copy)
    def _shallow_copy(self, values, name: Hashable = no_default):
        name = self.name if name is no_default else name

        if values.dtype.kind == "f":
            return Float64Index(values, name=name)
        # GH 46675 & 43885: If values is equally spaced, return a
        # more memory-compact RangeIndex instead of Int64Index
        unique_diffs = unique_deltas(values)
        if len(unique_diffs) == 1 and unique_diffs[0] != 0:
            diff = unique_diffs[0]
            new_range = range(values[0], values[-1] + diff, diff)
            return type(self)._simple_new(new_range, name=name)
        else:
            return Int64Index._simple_new(values, name=name)
