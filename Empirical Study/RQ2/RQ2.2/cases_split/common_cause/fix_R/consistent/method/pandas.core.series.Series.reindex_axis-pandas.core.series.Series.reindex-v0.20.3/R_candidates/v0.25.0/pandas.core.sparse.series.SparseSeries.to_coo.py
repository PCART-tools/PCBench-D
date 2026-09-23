    @Appender(SparseAccessor.to_coo.__doc__)
    def to_coo(self, row_levels=(0,), column_levels=(1,), sort_labels=False):
        A, rows, columns = _sparse_series_to_coo(
            self, row_levels, column_levels, sort_labels=sort_labels
        )
        return A, rows, columns
