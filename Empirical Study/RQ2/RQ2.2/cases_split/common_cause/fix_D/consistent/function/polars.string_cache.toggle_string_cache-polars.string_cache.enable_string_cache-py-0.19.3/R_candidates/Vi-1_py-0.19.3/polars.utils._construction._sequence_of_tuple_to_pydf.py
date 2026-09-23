@_sequence_to_pydf_dispatcher.register(tuple)
def _sequence_of_tuple_to_pydf(
    first_element: tuple[Any, ...],
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    orient: Orientation | None,
    infer_schema_length: int | None,
) -> PyDataFrame:
    # infer additional meta information if named tuple
    if is_namedtuple(first_element.__class__):
        if schema is None:
            schema = first_element._fields  # type: ignore[attr-defined]
            if len(first_element.__annotations__) == len(schema):
                schema = [
                    (name, py_type_to_dtype(tp, raise_unmatched=False))
                    for name, tp in first_element.__annotations__.items()
                ]
        elif orient is None:
            orient = "row"

    # ...then defer to generic sequence processing
    return _sequence_of_sequence_to_pydf(
        first_element,
        data=data,
        schema=schema,
        schema_overrides=schema_overrides,
        orient=orient,
        infer_schema_length=infer_schema_length,
    )
