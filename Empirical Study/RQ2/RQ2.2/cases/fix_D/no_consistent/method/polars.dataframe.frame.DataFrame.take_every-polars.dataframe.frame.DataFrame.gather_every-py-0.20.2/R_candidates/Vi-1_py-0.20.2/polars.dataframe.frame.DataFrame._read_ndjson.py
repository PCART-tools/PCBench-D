    @classmethod
    def _read_ndjson(
        cls,
        source: str | Path | IOBase | bytes,
        *,
        schema: SchemaDefinition | None = None,
        schema_overrides: SchemaDefinition | None = None,
        ignore_errors: bool = False,
    ) -> Self:
        """
        Read into a DataFrame from a newline delimited JSON file.

        Use `pl.read_ndjson` to dispatch to this method.

        See Also
        --------
        polars.io.read_ndjson

        """
        if isinstance(source, StringIO):
            source = BytesIO(source.getvalue().encode())
        elif isinstance(source, (str, Path)):
            source = normalize_filepath(source)

        self = cls.__new__(cls)
        self._df = PyDataFrame.read_ndjson(
            source,
            ignore_errors=ignore_errors,
            schema=schema,
            schema_overrides=schema_overrides,
        )
        return self
