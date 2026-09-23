    @classmethod
    def _scan_csv(
        cls,
        source: str | list[str] | list[Path],
        *,
        has_header: bool = True,
        separator: str = ",",
        comment_prefix: str | None = None,
        quote_char: str | None = '"',
        skip_rows: int = 0,
        dtypes: SchemaDict | None = None,
        schema: SchemaDict | None = None,
        null_values: str | Sequence[str] | dict[str, str] | None = None,
        missing_utf8_is_empty_string: bool = False,
        ignore_errors: bool = False,
        cache: bool = True,
        with_column_names: Callable[[list[str]], list[str]] | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
        n_rows: int | None = None,
        encoding: CsvEncoding = "utf8",
        low_memory: bool = False,
        rechunk: bool = True,
        skip_rows_after_header: int = 0,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        try_parse_dates: bool = False,
        eol_char: str = "\n",
        raise_if_empty: bool = True,
        truncate_ragged_lines: bool = True,
    ) -> Self:
        """
        Lazily read from a CSV file or multiple files via glob patterns.

        Use `pl.scan_csv` to dispatch to this method.

        See Also
        --------
        polars.io.scan_csv

        """
        dtype_list: list[tuple[str, PolarsDataType]] | None = None
        if dtypes is not None:
            dtype_list = []
            for k, v in dtypes.items():
                dtype_list.append((k, py_type_to_dtype(v)))
        processed_null_values = _process_null_values(null_values)

        if isinstance(source, list):
            sources = source
            source = None  # type: ignore[assignment]
        else:
            sources = []

        self = cls.__new__(cls)
        self._ldf = PyLazyFrame.new_from_csv(
            source,
            sources,
            separator,
            has_header,
            ignore_errors,
            skip_rows,
            n_rows,
            cache,
            dtype_list,
            low_memory,
            comment_prefix,
            quote_char,
            processed_null_values,
            missing_utf8_is_empty_string,
            infer_schema_length,
            with_column_names,
            rechunk,
            skip_rows_after_header,
            encoding,
            _prepare_row_count_args(row_count_name, row_count_offset),
            try_parse_dates,
            eol_char=eol_char,
            raise_if_empty=raise_if_empty,
            truncate_ragged_lines=truncate_ragged_lines,
            schema=schema,
        )
        return self
