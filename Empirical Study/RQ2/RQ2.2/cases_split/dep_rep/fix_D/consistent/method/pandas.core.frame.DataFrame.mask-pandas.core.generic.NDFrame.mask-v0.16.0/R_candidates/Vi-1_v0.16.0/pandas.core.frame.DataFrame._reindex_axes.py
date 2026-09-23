    def _reindex_axes(self, axes, level, limit, method, fill_value, copy):
        frame = self

        columns = axes['columns']
        if columns is not None:
            frame = frame._reindex_columns(columns, copy, level, fill_value,
                                           limit)

        index = axes['index']
        if index is not None:
            frame = frame._reindex_index(index, method, copy, level,
                                         fill_value, limit)

        return frame
