    def glimpse(
        self,
        *,
        max_items_per_column: int = 10,
        max_colname_length: int = 50,
        return_as_string: bool = False,
    ) -> str | None:
        """
        Return a dense preview of the DataFrame.

        The formatting shows one line per column so that wide dataframes display
        cleanly. Each line shows the column name, the data type, and the first
        few values.

        Parameters
        ----------
        max_items_per_column
            Maximum number of items to show per column.
        max_colname_length
            Maximum length of the displayed column names; values that exceed this
            value are truncated with a trailing ellipsis.
        return_as_string
            If True, return the preview as a string instead of printing to stdout.

        See Also
        --------
        describe, head, tail

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1.0, 2.8, 3.0],
        ...         "b": [4, 5, None],
        ...         "c": [True, False, True],
        ...         "d": [None, "b", "c"],
        ...         "e": ["usd", "eur", None],
        ...         "f": [date(2020, 1, 1), date(2021, 1, 2), date(2022, 1, 1)],
        ...     }
        ... )
        >>> df.glimpse()
        Rows: 3
        Columns: 6
        $ a  <f64> 1.0, 2.8, 3.0
        $ b  <i64> 4, 5, None
        $ c <bool> True, False, True
        $ d  <str> None, 'b', 'c'
        $ e  <str> 'usd', 'eur', None
        $ f <date> 2020-01-01, 2021-01-02, 2022-01-01

        """
        # always print at most this number of values (mainly ensures that
        # we do not cast long arrays to strings, which would be slow)
        max_n_values = min(max_items_per_column, self.height)
        schema = self.schema

        def _parse_column(col_name: str, dtype: PolarsDataType) -> tuple[str, str, str]:
            fn = repr if schema[col_name] == Utf8 else str
            values = self[:max_n_values][col_name].to_list()
            val_str = ", ".join(fn(v) for v in values)  # type: ignore[operator]
            if len(col_name) > max_colname_length:
                col_name = col_name[: (max_colname_length - 1)] + "…"
            return col_name, f"<{_dtype_str_repr(dtype)}>", val_str

        data = [_parse_column(s, dtype) for s, dtype in self.schema.items()]

        # determine column layout widths
        max_col_name = max((len(col_name) for col_name, _, _ in data))
        max_col_dtype = max((len(dtype_str) for _, dtype_str, _ in data))
        max_col_values = 100 - max_col_name - max_col_dtype

        # print header
        output = StringIO()
        output.write(f"Rows: {self.height}\nColumns: {self.width}\n")

        # print individual columns: one row per column
        for col_name, dtype_str, val_str in data:
            output.write(
                f"$ {col_name:<{max_col_name}}"
                f" {dtype_str:>{max_col_dtype}}"
                f" {val_str:<{min(len(val_str), max_col_values)}}\n"
            )

        s = output.getvalue()
        if return_as_string:
            return s

        print(s, end=None)
        return None
