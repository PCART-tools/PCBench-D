    @cache_readonly
    def _engine(
        self,
    ) -> libindex.IndexEngine | libindex.ExtensionEngine:
        # For base class (object dtype) we get ObjectEngine
        target_values = self._get_engine_target()
        if (
            isinstance(target_values, ExtensionArray)
            and self._engine_type is libindex.ObjectEngine
        ):
            return libindex.ExtensionEngine(target_values)

        target_values = cast(np.ndarray, target_values)
        # to avoid a reference cycle, bind `target_values` to a local variable, so
        # `self` is not passed into the lambda.
        if target_values.dtype == bool:
            return libindex.BoolEngine(target_values)
        elif target_values.dtype == np.complex64:
            return libindex.Complex64Engine(target_values)
        elif target_values.dtype == np.complex128:
            return libindex.Complex128Engine(target_values)

        # error: Argument 1 to "ExtensionEngine" has incompatible type
        # "ndarray[Any, Any]"; expected "ExtensionArray"
        return self._engine_type(target_values)  # type: ignore[arg-type]
