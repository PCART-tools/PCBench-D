    def item(self, row: int | None = None, column: int | str | None = None) -> Any:
        """
        Return the DataFrame as a scalar, or return the element at the given row/column.

        Parameters
        ----------
        row
            Optional row index.
        column
            Optional column index or name.

        See Also
        --------
        row: Get the values of a single row, either by index or by predicate.

        Notes
        -----
        If row/col not provided, this is equivalent to `df[0,0]`, with a check that
        the shape is (1,1). With row/col, this is equivalent to `df[row,col]`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> df.select((pl.col("a") * pl.col("b")).sum()).item()
        32
        >>> df.item(1, 1)
        5
        >>> df.item(2, "b")
        6

        """
        if row is None and column is None:
            if self.shape != (1, 1):
                raise ValueError(
                    "can only call `.item()` if the dataframe is of shape (1, 1),"
                    " or if explicit row/col values are provided;"
                    f" frame has shape {self.shape!r}"
                )
            return self._df.select_at_idx(0).get_index(0)

        elif row is None or column is None:
            raise ValueError("cannot call `.item()` with only one of `row` or `column`")

        s = (
            self._df.select_at_idx(column)
            if isinstance(column, int)
            else self._df.get_column(column)
        )
        if s is None:
            raise IndexError(f"column index {column!r} is out of bounds")
        return s.get_index_signed(row)
