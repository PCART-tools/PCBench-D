def numpy_to_pydf(
    data: np.ndarray[Any, Any],
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    orient: Orientation | None = None,
    nan_to_null: bool = False,
) -> PyDataFrame:
    """Construct a PyDataFrame from a numpy ndarray (including structured ndarrays)."""
    shape = data.shape

    if data.dtype.names is not None:
        structured_array, orient = True, "col"
        record_names = list(data.dtype.names)
        n_columns = len(record_names)
        for nm in record_names:
            shape = data[nm].shape
            if len(data[nm].shape) > 2:
                raise ValueError(
                    f"cannot create DataFrame from structured array with elements > 2D; shape[{nm!r}] = {shape}"
                )
        if not schema:
            schema = record_names
    else:
        # Unpack columns
        structured_array, record_names = False, []
        if shape == (0,):
            n_columns = 0

        elif len(shape) == 1:
            n_columns = 1

        elif len(shape) == 2:
            if orient is None and schema is None:
                # default convention; first axis is rows, second axis is columns
                n_columns = shape[1]
                orient = "row"

            elif orient is None and schema is not None:
                # infer orientation from 'schema' param; if square array
                # we maintain the default convention where first axis = rows
                n_schema_cols = len(schema)
                if n_schema_cols == shape[0] and n_schema_cols != shape[1]:
                    orient = "col"
                    n_columns = shape[0]
                else:
                    orient = "row"
                    n_columns = shape[1]

            elif orient == "row":
                n_columns = shape[1]
            elif orient == "col":
                n_columns = shape[0]
            else:
                raise ValueError(
                    f"orient must be one of {{'col', 'row', None}}; found {orient!r} instead"
                )
        else:
            raise ValueError(
                f"cannot create DataFrame from array with more than two dimensions; shape = {shape}"
            )

    if schema is not None and len(schema) != n_columns:
        raise ValueError("dimensions of 'schema' arg must match data dimensions")

    column_names, schema_overrides = _unpack_schema(
        schema, schema_overrides=schema_overrides, n_expected=n_columns
    )

    # Convert data to series
    if structured_array:
        data_series = [
            pl.Series(
                name=series_name,
                values=data[record_name],
                dtype=schema_overrides.get(record_name),
                nan_to_null=nan_to_null,
            )._s
            for series_name, record_name in zip(column_names, record_names)
        ]
    elif shape == (0,):
        data_series = []

    elif len(shape) == 1:
        data_series = [
            pl.Series(
                name=column_names[0],
                values=data,
                dtype=schema_overrides.get(column_names[0]),
                nan_to_null=nan_to_null,
            )._s
        ]
    else:
        if orient == "row":
            data_series = [
                pl.Series(
                    name=column_names[i],
                    values=data[:, i],
                    dtype=schema_overrides.get(column_names[i]),
                    nan_to_null=nan_to_null,
                )._s
                for i in range(n_columns)
            ]
        else:
            data_series = [
                pl.Series(
                    name=column_names[i],
                    values=data[i],
                    dtype=schema_overrides.get(column_names[i]),
                    nan_to_null=nan_to_null,
                )._s
                for i in range(n_columns)
            ]

    data_series = _handle_columns_arg(data_series, columns=column_names)
    return PyDataFrame(data_series)
