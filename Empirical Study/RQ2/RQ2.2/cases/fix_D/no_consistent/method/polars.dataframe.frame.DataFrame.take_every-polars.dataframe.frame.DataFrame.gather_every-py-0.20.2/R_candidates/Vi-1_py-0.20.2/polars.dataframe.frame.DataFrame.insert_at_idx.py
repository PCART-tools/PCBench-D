    @deprecate_renamed_function("insert_column", version="0.19.14")
    @deprecate_renamed_parameter("series", "column", version="0.19.14")
    def insert_at_idx(self, index: int, column: Series) -> Self:
        """
        Insert a Series at a certain column index. This operation is in place.

        .. deprecated:: 0.19.14
            This method has been renamed to :func:`insert_column`.

        Parameters
        ----------
        index
            Column to insert the new `Series` column.
        column
            `Series` to insert.
        """
        return self.insert_column(index, column)
