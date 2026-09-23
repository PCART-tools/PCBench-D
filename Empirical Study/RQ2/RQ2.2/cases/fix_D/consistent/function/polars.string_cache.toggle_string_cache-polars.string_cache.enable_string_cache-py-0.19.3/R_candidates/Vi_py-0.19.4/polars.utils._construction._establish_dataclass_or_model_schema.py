def _establish_dataclass_or_model_schema(
    first_element: Any,
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    model_fields: list[str] | None,
) -> tuple[bool, list[str], SchemaDict, SchemaDict]:
    """Shared utility code for establishing dataclasses/pydantic model cols/schema."""
    from dataclasses import asdict

    unpack_nested = False
    if schema:
        column_names, schema_overrides = _unpack_schema(
            schema, schema_overrides=schema_overrides
        )
        overrides = {col: schema_overrides.get(col, Unknown) for col in column_names}
    else:
        column_names = []
        overrides = {
            col: (py_type_to_dtype(tp, raise_unmatched=False) or Unknown)
            for col, tp in type_hints(first_element.__class__).items()
            if ((col in model_fields) if model_fields else (col != "__slots__"))
        }
        if schema_overrides:
            overrides.update(schema_overrides)
        elif not model_fields:
            dc_fields = set(asdict(first_element))
            schema_overrides = overrides = {
                nm: tp for nm, tp in overrides.items() if nm in dc_fields
            }
        else:
            schema_overrides = overrides

    for col, tp in overrides.items():
        if tp == Categorical:
            overrides[col] = Utf8
        elif not unpack_nested and (tp.base_type() in (Unknown, Struct)):
            unpack_nested = contains_nested(
                getattr(first_element, col, None),
                is_pydantic_model if model_fields else dataclasses.is_dataclass,  # type: ignore[arg-type]
            )

    if model_fields and len(model_fields) == len(overrides):
        overrides = dict(zip(model_fields, overrides.values()))

    return unpack_nested, column_names, schema_overrides, overrides
