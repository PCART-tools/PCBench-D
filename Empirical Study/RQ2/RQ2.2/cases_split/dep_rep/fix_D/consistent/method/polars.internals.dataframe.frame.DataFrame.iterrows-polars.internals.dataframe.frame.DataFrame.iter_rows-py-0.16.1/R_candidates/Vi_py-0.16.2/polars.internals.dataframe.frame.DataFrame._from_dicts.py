    @classmethod
    def _from_dicts(
        cls: type[DF],
        data: Sequence[dict[str, Any]],
        infer_schema_length: int | None = N_INFER_DEFAULT,
        schema: SchemaDefinition | None = None,
        schema_overrides: SchemaDict | None = None,
    ) -> DF:
        pydf = PyDataFrame.read_dicts(data, infer_schema_length, schema)
        if schema or schema_overrides:
            pydf = _post_apply_columns(
                pydf, list(schema or pydf.columns()), schema_overrides=schema_overrides
            )
        return cls._from_pydf(pydf)
