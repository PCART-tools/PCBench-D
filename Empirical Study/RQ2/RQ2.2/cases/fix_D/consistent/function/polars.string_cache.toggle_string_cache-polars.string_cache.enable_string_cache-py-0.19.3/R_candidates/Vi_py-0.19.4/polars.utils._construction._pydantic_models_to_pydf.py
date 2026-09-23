def _pydantic_models_to_pydf(
    first_element: Any,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    infer_schema_length: int | None,
    **kwargs: Any,
) -> PyDataFrame:
    """Initialise DataFrame from pydantic model objects."""
    import pydantic  # note: must already be available in the env here

    old_pydantic = parse_version(pydantic.__version__) < parse_version("2.0")
    model_fields = list(
        first_element.__fields__ if old_pydantic else first_element.model_fields
    )
    (
        unpack_nested,
        column_names,
        schema_overrides,
        overrides,
    ) = _establish_dataclass_or_model_schema(
        first_element, schema, schema_overrides, model_fields
    )
    if unpack_nested:
        # note: this is an *extremely* slow path, due to the requirement to
        # use pydantic's 'dict()' method to properly unpack nested models
        dicts = (
            [md.dict() for md in data]
            if old_pydantic
            else [md.model_dump(mode="python") for md in data]
        )
        pydf = PyDataFrame.read_dicts(dicts, infer_schema_length)

    elif len(model_fields) > 50:
        # 'read_rows' is the faster codepath for models with a lot of fields...
        get_values = itemgetter(*model_fields)
        rows = [get_values(md.__dict__) for md in data]
        pydf = PyDataFrame.read_rows(rows, infer_schema_length, overrides)
    else:
        # ...and 'read_dicts' is faster otherwise
        dicts = [md.__dict__ for md in data]
        pydf = PyDataFrame.read_dicts(dicts, infer_schema_length, overrides)

    if overrides:
        structs = {c: tp for c, tp in overrides.items() if isinstance(tp, Struct)}
        pydf = _post_apply_columns(pydf, column_names, structs, schema_overrides)

    return pydf
