@_sequence_to_pydf_dispatcher.register(list)
def _sequence_of_sequence_to_pydf(
    first_element: Sequence[Any] | np.ndarray[Any, Any],
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    orient: Orientation | None,
    infer_schema_length: int | None,
) -> PyDataFrame:
    if orient is None:
        # note: limit type-checking to smaller data; larger values are much more
        # likely to indicate col orientation anyway, so minimise extra checks.
        if len(first_element) > 1000:
            orient = "col" if schema and len(schema) == len(data) else "row"
        elif (schema is not None and len(schema) == len(data)) or not schema:
            # check if element types in the first 'row' resolve to a single dtype.
            row_types = {type(value) for value in first_element if value is not None}
            if int in row_types and float in row_types:
                row_types.discard(int)
            orient = "col" if len(row_types) == 1 else "row"
        else:
            orient = "row"

    if orient == "row":
        column_names, schema_overrides = _unpack_schema(
            schema, schema_overrides=schema_overrides, n_expected=len(first_element)
        )
        local_schema_override = (
            include_unknowns(schema_overrides, column_names) if schema_overrides else {}
        )
        if column_names and len(first_element) != len(column_names):
            raise ShapeError("the row data does not match the number of columns")

        unpack_nested = False
        for col, tp in local_schema_override.items():
            if tp == Categorical:
                local_schema_override[col] = Utf8
            elif not unpack_nested and (tp.base_type() in (Unknown, Struct)):
                unpack_nested = contains_nested(
                    getattr(first_element, col, None).__class__, is_namedtuple
                )

        if unpack_nested:
            dicts = [nt_unpack(d) for d in data]
            pydf = PyDataFrame.read_dicts(dicts, infer_schema_length)
        else:
            pydf = PyDataFrame.read_rows(
                data,
                infer_schema_length,
                local_schema_override or None,
            )
        if column_names or schema_overrides:
            pydf = _post_apply_columns(
                pydf, column_names, schema_overrides=schema_overrides
            )
        return pydf

    if orient == "col" or orient is None:
        column_names, schema_overrides = _unpack_schema(
            schema, schema_overrides=schema_overrides, n_expected=len(data)
        )
        data_series: list[PySeries] = [
            pl.Series(
                column_names[i], element, schema_overrides.get(column_names[i])
            )._s
            for i, element in enumerate(data)
        ]
        return PyDataFrame(data_series)

    raise ValueError(
        f"orient must be one of {{'col', 'row', None}}, got {orient!r} instead"
    )
