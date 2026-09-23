    def glimpse(self: DF) -> str:
        """
        Print a dense preview of the dataframe.

        Printing is done one line per column, so wide dataframes show nicely. Each
        line will show the column name, the data type and the first few values.

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
        >>> print(df.glimpse())
        Rows: 3
        Columns: 6
        $ a  <f64> 1.0, 2.8, 3.0
        $ b  <i64> 4, 5, None
        $ c <bool> True, False, True
        $ d  <str> None, b, c
        $ e  <str> usd, eur, None
        $ f <date> 2020-01-01, 2021-01-02, 2022-01-01

        """
        # always print at most this number of values, mainly used to ensure
        # we do not cast long arrays to strings which would be very slow
        max_num_values = min(10, self.height)

        def _parse_column(col_name: str, dtype: PolarsDataType) -> tuple[str, str, str]:
            dtype_str = (
                f"<{DataTypeClass._string_repr(dtype)}>"
                if isinstance(dtype, DataTypeClass)
                else f"<{dtype._string_repr()}>"
            )
            val = self[:max_num_values][col_name].to_list()
            val_str = ", ".join(map(str, val))
            return col_name, dtype_str, val_str

        data = [_parse_column(s, dtype) for s, dtype in self.schema.items()]

        # we make the first column as small as possible by taking the longest
        # column name
        max_col_name = max((len(col_name) for col_name, _, _ in data))

        # dtype string
        max_col_dtype = max((len(dtype_str) for _, dtype_str, _ in data))

        # limit the amount of data printed such that total width is fixed
        max_col_values = 100 - max_col_name - max_col_dtype

        output = StringIO()
        # print header
        output.write(f"Rows: {self.height}\nColumns: {self.width}\n")

        # print individual columns: one row per column
        for col_name, dtype_str, val_str in data:
            output.write(
                f"$ {col_name:<{max_col_name}}"
                f" {dtype_str:>{max_col_dtype}}"
                f" {val_str:<{min(len(val_str), max_col_values)}}\n"
            )

        return output.getvalue()
