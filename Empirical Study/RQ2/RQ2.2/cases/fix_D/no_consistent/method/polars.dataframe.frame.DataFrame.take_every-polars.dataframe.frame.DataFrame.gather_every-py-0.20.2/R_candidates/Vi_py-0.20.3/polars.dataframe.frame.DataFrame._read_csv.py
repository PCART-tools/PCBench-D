    @classmethod
    def _read_csv(
        cls,
        source: str | Path | IO[bytes] | bytes,
        *,
        has_header: bool = True,
        columns: Sequence[int] | Sequence[str] | None = None,
        separator: str = ",",
        comment_prefix: str | None = None,
        quote_char: str | None = '"',
        skip_rows: int = 0,
        dtypes: None | (SchemaDict | Sequence[PolarsDataType]) = None,
        schema: None | SchemaDict = None,
        null_values: str | Sequence[str] | dict[str, str] | None = None,
        missing_utf8_is_empty_string: bool = False,
        ignore_errors: bool = False,
        try_parse_dates: bool = False,
        n_threads: int | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
        batch_size: int = 8192,
        n_rows: int | None = None,
        encoding: CsvEncoding = "utf8",
        low_memory: bool = False,
        rechunk: bool = True,
        skip_rows_after_header: int = 0,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        sample_size: int = 1024,
        eol_char: str = "\n",
        raise_if_empty: bool = True,
        truncate_ragged_lines: bool = False,
    ) -> DataFrame:
        """
        Read a CSV file into a DataFrame.

        Use `pl.read_csv` to dispatch to this method.

        See Also
        --------
        polars.io.read_csv

        """
        self = cls.__new__(cls)

        path: str | None
        if isinstance(source, (str, Path)):
            path = normalize_filepath(source)
        else:
            path = None
            if isinstance(source, BytesIO):
                source = source.getvalue()
            if isinstance(source, StringIO):
                source = source.getvalue().encode()

        dtype_list: Sequence[tuple[str, PolarsDataType]] | None = None
        dtype_slice: Sequence[PolarsDataType] | None = None
        if dtypes is not None:
            if isinstance(dtypes, dict):
                dtype_list = []
                for k, v in dtypes.items():
                    dtype_list.append((k, py_type_to_dtype(v)))
            elif isinstance(dtypes, Sequence):
                dtype_slice = dtypes
            else:
                raise TypeError(
                    f"`dtypes` should be of type list or dict, got {type(dtypes).__name__!r}"
                )

        processed_null_values = _process_null_values(null_values)

        if isinstance(columns, str):
            columns = [columns]
        if isinstance(source, str) and _is_glob_pattern(source):
            dtypes_dict = None
            if dtype_list is not None:
                dtypes_dict = dict(dtype_list)
            if dtype_slice is not None:
                raise ValueError(
                    "cannot use glob patterns and unnamed dtypes as `dtypes` argument"
                    "\n\nUse `dtypes`: Mapping[str, Type[DataType]]"
                )
            from polars import scan_csv

            scan = scan_csv(
                source,
                has_header=has_header,
                separator=separator,
                comment_prefix=comment_prefix,
                quote_char=quote_char,
                skip_rows=skip_rows,
                dtypes=dtypes_dict,
                schema=schema,
                null_values=null_values,
                missing_utf8_is_empty_string=missing_utf8_is_empty_string,
                ignore_errors=ignore_errors,
                infer_schema_length=infer_schema_length,
                n_rows=n_rows,
                low_memory=low_memory,
                rechunk=rechunk,
                skip_rows_after_header=skip_rows_after_header,
                row_count_name=row_count_name,
                row_count_offset=row_count_offset,
                eol_char=eol_char,
                raise_if_empty=raise_if_empty,
                truncate_ragged_lines=truncate_ragged_lines,
            )
            if columns is None:
                return scan.collect()
            elif is_str_sequence(columns, allow_str=False):
                return scan.select(columns).collect()
            else:
                raise ValueError(
                    "cannot use glob patterns and integer based projection as `columns` argument"
                    "\n\nUse columns: List[str]"
                )

        projection, columns = handle_projection_columns(columns)

        self._df = PyDataFrame.read_csv(
            source,
            infer_schema_length,
            batch_size,
            has_header,
            ignore_errors,
            n_rows,
            skip_rows,
            projection,
            separator,
            rechunk,
            columns,
            encoding,
            n_threads,
            path,
            dtype_list,
            dtype_slice,
            low_memory,
            comment_prefix,
            quote_char,
            processed_null_values,
            missing_utf8_is_empty_string,
            try_parse_dates,
            skip_rows_after_header,
            _prepare_row_count_args(row_count_name, row_count_offset),
            sample_size=sample_size,
            eol_char=eol_char,
            raise_if_empty=raise_if_empty,
            truncate_ragged_lines=truncate_ragged_lines,
            schema=schema,
        )
        return self
