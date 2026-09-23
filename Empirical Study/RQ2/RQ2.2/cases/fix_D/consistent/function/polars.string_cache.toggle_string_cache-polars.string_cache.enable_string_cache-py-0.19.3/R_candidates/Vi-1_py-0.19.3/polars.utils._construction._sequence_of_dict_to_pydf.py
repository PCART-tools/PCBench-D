@_sequence_to_pydf_dispatcher.register(dict)
def _sequence_of_dict_to_pydf(
    first_element: Any,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    infer_schema_length: int | None,
    **kwargs: Any,
) -> PyDataFrame:
    column_names, schema_overrides = _unpack_schema(
        schema, schema_overrides=schema_overrides
    )
    dicts_schema = (
        include_unknowns(schema_overrides, column_names or list(schema_overrides))
        if column_names
        else None
    )
    pydf = PyDataFrame.read_dicts(data, infer_schema_length, dicts_schema)

    # TODO: we can remove this `schema_overrides` block completely
    #  once https://github.com/pola-rs/polars/issues/11044 is fixed
    if schema_overrides:
        pydf = _post_apply_columns(
            pydf,
            columns=column_names,
            schema_overrides=schema_overrides,
        )
    return pydf
