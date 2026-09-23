    def set_sorted(
        self,
        column: str,
        *,
        descending: bool = False,
    ) -> LazyFrame:
        """
        Indicate that one or multiple columns are sorted.

        This can speed up future operations.

        Parameters
        ----------
        column
            Columns that are sorted
        descending
            Whether the columns are sorted in descending order.

        Warnings
        --------
        This can lead to incorrect results if the data is NOT sorted!!
        Use with care!

        """
        # NOTE: Only accepts 1 column on purpose! User think they are sorted by
        # the combined multicolumn values.
        if not isinstance(column, str):
            msg = "expected a 'str' for argument 'column' in 'set_sorted'"
            raise TypeError(msg)
        return self.with_columns(F.col(column).set_sorted(descending=descending))
