    @classmethod
    def _scan_python_function(
        cls,
        schema: pa.schema | Mapping[str, PolarsDataType],
        scan_fn: Any,
        *,
        pyarrow: bool = False,
    ) -> LazyFrame:
        self = cls.__new__(cls)
        if isinstance(schema, Mapping):
            self._ldf = PyLazyFrame.scan_from_python_function_pl_schema(
                list(schema.items()), scan_fn, pyarrow
            )
        else:
            self._ldf = PyLazyFrame.scan_from_python_function_arrow_schema(
                list(schema), scan_fn, pyarrow
            )
        return self
