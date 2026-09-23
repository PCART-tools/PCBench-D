    def __init__(
        self,
        data: FrameInitTypes | None = None,
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
        strict: bool = True,
        orient: Orientation | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
        nan_to_null: bool = False,
    ):
        if data is None:
            self._df = dict_to_pydf(
                {}, schema=schema, schema_overrides=schema_overrides
            )

        elif isinstance(data, dict):
            self._df = dict_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                strict=strict,
                nan_to_null=nan_to_null,
            )

        elif isinstance(data, (list, tuple, Sequence)):
            self._df = sequence_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                strict=strict,
                orient=orient,
                infer_schema_length=infer_schema_length,
            )

        elif isinstance(data, pl.Series):
            self._df = series_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides, strict=strict
            )

        elif _check_for_numpy(data) and isinstance(data, np.ndarray):
            self._df = numpy_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                strict=strict,
                orient=orient,
                nan_to_null=nan_to_null,
            )

        elif _check_for_pyarrow(data) and isinstance(data, pa.Table):
            self._df = arrow_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides, strict=strict
            )

        elif _check_for_pandas(data) and isinstance(data, pd.DataFrame):
            self._df = pandas_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides, strict=strict
            )

        elif not isinstance(data, Sized) and isinstance(data, (Generator, Iterable)):
            self._df = iterable_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                strict=strict,
                orient=orient,
                infer_schema_length=infer_schema_length,
            )

        elif isinstance(data, pl.DataFrame):
            self._df = dataframe_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides, strict=strict
            )
        else:
            msg = (
                f"DataFrame constructor called with unsupported type {type(data).__name__!r}"
                " for the `data` parameter"
            )
            raise TypeError(msg)
