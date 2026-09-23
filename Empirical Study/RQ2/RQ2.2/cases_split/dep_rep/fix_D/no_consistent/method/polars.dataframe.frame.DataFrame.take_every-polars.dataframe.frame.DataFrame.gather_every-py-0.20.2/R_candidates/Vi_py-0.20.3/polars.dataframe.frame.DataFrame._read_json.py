    @classmethod
    def _read_json(
        cls,
        source: str | Path | IOBase | bytes,
        *,
        infer_schema_length: int | None = N_INFER_DEFAULT,
        schema: SchemaDefinition | None = None,
        schema_overrides: SchemaDefinition | None = None,
    ) -> Self:
        """
        Read into a DataFrame from a JSON file.

        Use `pl.read_json` to dispatch to this method.

        See Also
        --------
        polars.io.read_json

        """
        if isinstance(source, StringIO):
            source = BytesIO(source.getvalue().encode())
        elif isinstance(source, (str, Path)):
            source = normalize_filepath(source)

        self = cls.__new__(cls)
        self._df = PyDataFrame.read_json(
            source,
            infer_schema_length=infer_schema_length,
            schema=schema,
            schema_overrides=schema_overrides,
        )
        return self
