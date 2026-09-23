    @classmethod
    def _scan_ndjson(
        cls,
        source: str | Path | list[str] | list[Path],
        *,
        infer_schema_length: int | None = None,
        schema: SchemaDefinition | None = None,
        batch_size: int | None = None,
        n_rows: int | None = None,
        low_memory: bool = False,
        rechunk: bool = True,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
    ) -> Self:
        """
        Lazily read from a newline delimited JSON file.

        Use `pl.scan_ndjson` to dispatch to this method.

        See Also
        --------
        polars.io.scan_ndjson

        """
        if isinstance(source, (str, Path)):
            source = normalize_filepath(source)
            sources = []
        else:
            sources = [normalize_filepath(source) for source in source]
            source = None  # type: ignore[assignment]

        self = cls.__new__(cls)
        self._ldf = PyLazyFrame.new_from_ndjson(
            source,
            sources,
            infer_schema_length,
            schema,
            batch_size,
            n_rows,
            low_memory,
            rechunk,
            _prepare_row_count_args(row_count_name, row_count_offset),
        )
        return self
