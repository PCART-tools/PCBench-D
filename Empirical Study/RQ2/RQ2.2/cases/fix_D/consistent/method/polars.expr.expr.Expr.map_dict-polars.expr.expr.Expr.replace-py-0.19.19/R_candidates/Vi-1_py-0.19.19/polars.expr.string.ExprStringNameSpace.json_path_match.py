    def json_path_match(self, json_path: str) -> Expr:
        """
        Extract the first match of JSON string with the provided JSONPath expression.

        Throws errors if invalid JSON strings are encountered.
        All return values will be cast to :class:`Utf8` regardless of the original
        value.

        Documentation on JSONPath standard can be found
        `here <https://goessner.net/articles/JsonPath/>`_.

        Parameters
        ----------
        json_path
            A valid JSON path query string.

        Returns
        -------
        Expr
            Expression of data type :class:`Utf8`. Contains null values if original
            value is null or the json_path returns nothing.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"json_val": ['{"a":"1"}', None, '{"a":2}', '{"a":2.1}', '{"a":true}']}
        ... )
        >>> df.with_columns(matched=pl.col("json_val").str.json_path_match("$.a"))
        shape: (5, 2)
        ┌────────────┬─────────┐
        │ json_val   ┆ matched │
        │ ---        ┆ ---     │
        │ str        ┆ str     │
        ╞════════════╪═════════╡
        │ {"a":"1"}  ┆ 1       │
        │ null       ┆ null    │
        │ {"a":2}    ┆ 2       │
        │ {"a":2.1}  ┆ 2.1     │
        │ {"a":true} ┆ true    │
        └────────────┴─────────┘

        """
        return wrap_expr(self._pyexpr.str_json_path_match(json_path))
