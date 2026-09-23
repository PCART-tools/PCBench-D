    def set_sorted(
        self,
        column: str | Iterable[str],
        *more_columns: str,
        descending: bool = False,
    ) -> Self:
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
        columns = parse_as_list_of_expressions(column, *more_columns)

        return self.with_columns(
            [wrap_expr(e).set_sorted(descending=descending) for e in columns]
        )
