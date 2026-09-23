def _dataclasses_or_models_to_pydf(
    first_element: Any,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    infer_schema_length: int | None,
    **kwargs: Any,
) -> PyDataFrame:
    """Initialise DataFrame from python dataclass and/or pydantic model objects."""
    from dataclasses import asdict, astuple

    from_model = kwargs.get("pydantic_model")
    unpack_nested = False
    if schema:
        column_names, schema_overrides = _unpack_schema(
            schema, schema_overrides=schema_overrides
        )
        schema_override = {
            col: schema_overrides.get(col, Unknown) for col in column_names
        }
    else:
        column_names = []
        schema_override = {
            col: (py_type_to_dtype(tp, raise_unmatched=False) or Unknown)
            for col, tp in type_hints(first_element.__class__).items()
            if col not in ("__slots__", "__pydantic_root_model__")
        }
        if schema_overrides:
            schema_override.update(schema_overrides)
        elif not from_model:
            dc_fields = set(asdict(first_element))
            schema_overrides = schema_override = {
                nm: tp for nm, tp in schema_override.items() if nm in dc_fields
            }
        else:
            schema_overrides = schema_override

    for col, tp in schema_override.items():
        if tp == Categorical:
            schema_override[col] = Utf8
        elif not unpack_nested and (tp.base_type() in (Unknown, Struct)):
            unpack_nested = contains_nested(
                getattr(first_element, col, None),
                is_pydantic_model if from_model else dataclasses.is_dataclass,  # type: ignore[arg-type]
            )

    if unpack_nested:
        if from_model:
            dicts = (
                [md.model_dump(mode="python") for md in data]
                if hasattr(first_element, "model_dump")
                else [md.dict() for md in data]
            )
        else:
            dicts = [asdict(md) for md in data]
        pydf = PyDataFrame.read_dicts(dicts, infer_schema_length)
    else:
        rows = (
            [tuple(md.__dict__.values()) for md in data]
            if from_model
            else [astuple(dc) for dc in data]
        )
        pydf = PyDataFrame.read_rows(rows, infer_schema_length, schema_override or None)

    if schema_override:
        structs = {c: tp for c, tp in schema_override.items() if isinstance(tp, Struct)}
        pydf = _post_apply_columns(pydf, column_names, structs, schema_overrides)

    return pydf
