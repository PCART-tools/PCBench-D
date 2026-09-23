    @deprecate_renamed_function("replace_column", version="0.19.14")
    @deprecate_renamed_parameter("series", "new_column", version="0.19.14")
    def replace_at_idx(self, index: int, new_column: Series) -> Self:
        """
        Replace a column at an index location.

        .. deprecated:: 0.19.14
            This method has been renamed to :func:`replace_column`.

        Parameters
        ----------
        index
            Column index.
        new_column
            Series that will replace the column.
        """
        return self.replace_column(index, new_column)
