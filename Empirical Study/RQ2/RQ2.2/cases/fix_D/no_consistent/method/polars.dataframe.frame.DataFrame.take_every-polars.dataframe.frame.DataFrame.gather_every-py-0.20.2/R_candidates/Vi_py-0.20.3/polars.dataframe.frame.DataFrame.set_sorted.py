    def set_sorted(
        self,
        column: str | Iterable[str],
        *more_columns: str,
        descending: bool = False,
    ) -> DataFrame:
        """
        Indicate that one or multiple columns are sorted.

        Parameters
        ----------
        column
            Columns that are sorted
        more_columns
            Additional columns that are sorted, specified as positional arguments.
        descending
            Whether the columns are sorted in descending order.
        """
        return (
            self.lazy()
            .set_sorted(column, *more_columns, descending=descending)
            .collect(_eager=True)
        )
