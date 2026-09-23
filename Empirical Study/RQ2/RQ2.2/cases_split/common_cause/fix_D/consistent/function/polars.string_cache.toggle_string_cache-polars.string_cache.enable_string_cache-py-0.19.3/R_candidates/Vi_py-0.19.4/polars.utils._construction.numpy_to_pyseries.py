def numpy_to_pyseries(
    name: str,
    values: np.ndarray[Any, Any],
    *,
    strict: bool = True,
    nan_to_null: bool = False,
) -> PySeries:
    """Construct a PySeries from a numpy array."""
    if not values.flags["C_CONTIGUOUS"]:
        values = np.array(values)

    if len(values.shape) == 1:
        values, dtype = numpy_values_and_dtype(values)
        constructor = numpy_type_to_constructor(dtype)
        return constructor(
            name, values, nan_to_null if dtype in (np.float32, np.float64) else strict
        )
    elif len(values.shape) == 2:
        pyseries_container = []
        for row in range(values.shape[0]):
            pyseries_container.append(
                numpy_to_pyseries(
                    "", values[row, :], strict=strict, nan_to_null=nan_to_null
                )
            )
        return PySeries.new_series_list(name, pyseries_container, _strict=False)
    else:
        return PySeries.new_object(name, values, strict)
