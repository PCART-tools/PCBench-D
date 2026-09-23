    def _count_level(self, level, axis=0, numeric_only=False):
        if numeric_only:
            frame = self._get_numeric_data()
        else:
            frame = self

        if axis == 1:
            frame = frame.T

        if not isinstance(frame.index, MultiIndex):
            raise TypeError("Can only count levels on hierarchical %s." %
                            self._get_axis_name(axis))

        # python 2.5
        mask = notnull(frame.values).view(np.uint8)

        if isinstance(level, compat.string_types):
            level = self.index._get_level_number(level)

        level_index = frame.index.levels[level]
        labels = com._ensure_int64(frame.index.labels[level])
        counts = lib.count_level_2d(mask, labels, len(level_index))

        result = DataFrame(counts, index=level_index,
                           columns=frame.columns)

        if axis == 1:
            return result.T
        else:
            return result
