    @deprecated_alias(columns="schema")
    def __init__(
        self,
        data: (
            Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | pli.Series]
            | Sequence[Any]
            | np.ndarray[Any, Any]
            | pa.Table
            | pd.DataFrame
            | pli.Series
            | None
        ) = None,
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
        orient: Orientation | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
    ):
        if data is None:
            self._df = dict_to_pydf(
                {}, schema=schema, schema_overrides=schema_overrides
            )

        elif isinstance(data, dict):
            self._df = dict_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides
            )

        elif isinstance(data, (list, tuple, Sequence)):
            self._df = sequence_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                orient=orient,
                infer_schema_length=infer_schema_length,
            )
        elif isinstance(data, pli.Series):
            self._df = series_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides
            )

        elif _check_for_numpy(data) and isinstance(data, np.ndarray):
            self._df = numpy_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides, orient=orient
            )

        elif _check_for_pyarrow(data) and isinstance(data, pa.Table):
            self._df = arrow_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides
            )

        elif _check_for_pandas(data) and isinstance(data, pd.DataFrame):
            self._df = pandas_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides
            )

        elif not isinstance(data, Sized) and isinstance(data, (Generator, Iterable)):
            self._df = iterable_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                orient=orient,
                infer_schema_length=infer_schema_length,
            )
        else:
            raise ValueError(
                f"DataFrame constructor called with unsupported type; got {type(data)}"
            )
