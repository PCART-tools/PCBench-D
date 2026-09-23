    def _count_level(self, level, axis=0, numeric_only=False):
        if numeric_only:
            frame = self._get_numeric_data()
        else:
            frame = self

        count_axis = frame._get_axis(axis)
        agg_axis = frame._get_agg_axis(axis)

        if not isinstance(count_axis, MultiIndex):
            raise TypeError("Can only count levels on hierarchical %s." %
                            self._get_axis_name(axis))

        if frame._is_mixed_type:
            # Since we have mixed types, calling notnull(frame.values) might
            # upcast everything to object
            mask = notnull(frame).values
        else:
            # But use the speedup when we have homogeneous dtypes
            mask = notnull(frame.values)

        if axis == 1:
            # We're transposing the mask rather than frame to avoid potential
            # upcasts to object, which induces a ~20x slowdown
            mask = mask.T

        if isinstance(level, compat.string_types):
            level = count_axis._get_level_number(level)

        level_index = count_axis.levels[level]
        labels = _ensure_int64(count_axis.labels[level])
        counts = lib.count_level_2d(mask, labels, len(level_index), axis=0)

        result = DataFrame(counts, index=level_index, columns=agg_axis)

        if axis == 1:
            # Undo our earlier transpose
            return result.T
        else:
            return result
