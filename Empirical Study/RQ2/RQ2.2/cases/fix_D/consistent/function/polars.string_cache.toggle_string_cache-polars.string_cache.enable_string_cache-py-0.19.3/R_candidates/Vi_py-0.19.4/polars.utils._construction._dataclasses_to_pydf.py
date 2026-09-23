def _dataclasses_to_pydf(
    first_element: Any,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    infer_schema_length: int | None,
    **kwargs: Any,
) -> PyDataFrame:
    """Initialise DataFrame from python dataclasses."""
    from dataclasses import asdict, astuple

    (
        unpack_nested,
        column_names,
        schema_overrides,
        overrides,
    ) = _establish_dataclass_or_model_schema(
        first_element, schema, schema_overrides, model_fields=None
    )
    if unpack_nested:
        dicts = [asdict(md) for md in data]
        pydf = PyDataFrame.read_dicts(dicts, infer_schema_length)
    else:
        rows = [astuple(dc) for dc in data]
        pydf = PyDataFrame.read_rows(rows, infer_schema_length, overrides or None)

    if overrides:
        structs = {c: tp for c, tp in overrides.items() if isinstance(tp, Struct)}
        pydf = _post_apply_columns(pydf, column_names, structs, schema_overrides)

    return pydf
