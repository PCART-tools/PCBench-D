@singledispatch
def _sequence_to_pydf_dispatcher(
    first_element: Any,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    orient: Orientation | None,
    infer_schema_length: int | None,
) -> PyDataFrame:
    # note: ONLY python-native data should participate in singledispatch registration
    # via top-level decorators. third-party libraries (such as numpy/pandas) should
    # first be identified inline (here) and THEN registered for dispatch dynamically
    # so as not to break lazy-loading behaviour.

    common_params = {
        "data": data,
        "schema": schema,
        "schema_overrides": schema_overrides,
        "orient": orient,
        "infer_schema_length": infer_schema_length,
    }

    to_pydf: Callable[..., PyDataFrame]
    register_with_singledispatch = True

    if isinstance(first_element, Generator):
        to_pydf = _sequence_of_sequence_to_pydf
        data = [list(row) for row in data]
        first_element = data[0]
        register_with_singledispatch = False

    elif isinstance(first_element, pl.Series):
        to_pydf = _sequence_of_series_to_pydf

    elif _check_for_numpy(first_element) and isinstance(first_element, np.ndarray):
        to_pydf = _sequence_of_numpy_to_pydf

    elif _check_for_pandas(first_element) and isinstance(
        first_element, (pd.Series, pd.DatetimeIndex)
    ):
        to_pydf = _sequence_of_pandas_to_pydf

    elif dataclasses.is_dataclass(first_element):
        to_pydf = _dataclasses_or_models_to_pydf

    elif is_pydantic_model(first_element):
        to_pydf = partial(_dataclasses_or_models_to_pydf, pydantic_model=True)
    else:
        to_pydf = _sequence_of_elements_to_pydf

    if register_with_singledispatch:
        _sequence_to_pydf_dispatcher.register(type(first_element), to_pydf)

    common_params["first_element"] = first_element
    return to_pydf(**common_params)
