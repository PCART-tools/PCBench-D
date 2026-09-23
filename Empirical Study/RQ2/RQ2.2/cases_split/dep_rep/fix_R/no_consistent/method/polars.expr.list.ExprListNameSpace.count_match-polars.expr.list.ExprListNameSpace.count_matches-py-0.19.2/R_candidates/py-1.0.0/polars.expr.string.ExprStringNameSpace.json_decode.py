    def json_decode(
        self,
        dtype: PolarsDataType | None = None,
        *,
        infer_schema_length: int | None = N_INFER_DEFAULT,
    ) -> Expr:
        """
        Parse string values as JSON.

        Throws an error if invalid JSON strings are encountered.

        Parameters
        ----------
        dtype
            The dtype to cast the extracted value to. If None, the dtype will be
            inferred from the JSON value.
        infer_schema_length
            The maximum number of rows to scan for schema inference.
            If set to `None`, the full data may be scanned *(this is slow)*.

        See Also
        --------
        json_path_match : Extract the first match of json string with provided JSONPath
            expression.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"json": ['{"a":1, "b": true}', None, '{"a":2, "b": false}']}
        ... )
        >>> dtype = pl.Struct([pl.Field("a", pl.Int64), pl.Field("b", pl.Boolean)])
        >>> df.with_columns(decoded=pl.col("json").str.json_decode(dtype))
        shape: (3, 2)
        ┌─────────────────────┬─────────────┐
        │ json                ┆ decoded     │
        │ ---                 ┆ ---         │
        │ str                 ┆ struct[2]   │
        ╞═════════════════════╪═════════════╡
        │ {"a":1, "b": true}  ┆ {1,true}    │
        │ null                ┆ {null,null} │
        │ {"a":2, "b": false} ┆ {2,false}   │
        └─────────────────────┴─────────────┘
        """
        if dtype is not None:
            dtype = parse_into_dtype(dtype)
        return wrap_expr(self._pyexpr.str_json_decode(dtype, infer_schema_length))
