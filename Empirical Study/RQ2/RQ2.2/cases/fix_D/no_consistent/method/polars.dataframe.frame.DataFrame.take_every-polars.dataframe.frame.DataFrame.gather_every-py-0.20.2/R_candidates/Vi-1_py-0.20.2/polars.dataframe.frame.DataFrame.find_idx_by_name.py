    @deprecate_renamed_function("get_column_index", version="0.19.14")
    def find_idx_by_name(self, name: str) -> int:
        """
        Find the index of a column by name.

        .. deprecated:: 0.19.14
            This method has been renamed to :func:`get_column_index`.

        Parameters
        ----------
        name
            Name of the column to find.
        """
        return self.get_column_index(name)
