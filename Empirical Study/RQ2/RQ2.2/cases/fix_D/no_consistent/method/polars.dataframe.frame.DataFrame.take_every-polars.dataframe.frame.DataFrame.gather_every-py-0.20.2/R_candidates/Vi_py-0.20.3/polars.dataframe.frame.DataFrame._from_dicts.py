    @classmethod
    def _from_dicts(
        cls,
        data: Sequence[dict[str, Any]],
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
    ) -> Self:
        pydf = PyDataFrame.read_dicts(
            data, infer_schema_length, schema, schema_overrides
        )
        if schema or schema_overrides:
            pydf = _post_apply_columns(
                pydf, list(schema or pydf.columns()), schema_overrides=schema_overrides
            )
        return cls._from_pydf(pydf)
