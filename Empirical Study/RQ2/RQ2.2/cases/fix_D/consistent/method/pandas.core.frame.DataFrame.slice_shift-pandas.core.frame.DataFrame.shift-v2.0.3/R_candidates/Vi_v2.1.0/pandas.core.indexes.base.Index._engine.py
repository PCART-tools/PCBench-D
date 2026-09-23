    @cache_readonly
    def _engine(
        self,
    ) -> libindex.IndexEngine | libindex.ExtensionEngine | libindex.MaskedIndexEngine:
        # For base class (object dtype) we get ObjectEngine
        target_values = self._get_engine_target()

        if isinstance(self._values, ArrowExtensionArray) and self.dtype.kind in "Mm":
            import pyarrow as pa

            pa_type = self._values._pa_array.type
            if pa.types.is_timestamp(pa_type):
                target_values = self._values._to_datetimearray()
                return libindex.DatetimeEngine(target_values._ndarray)
            elif pa.types.is_duration(pa_type):
                target_values = self._values._to_timedeltaarray()
                return libindex.TimedeltaEngine(target_values._ndarray)

        if isinstance(target_values, ExtensionArray):
            if isinstance(target_values, (BaseMaskedArray, ArrowExtensionArray)):
                try:
                    return _masked_engines[target_values.dtype.name](target_values)
                except KeyError:
                    # Not supported yet e.g. decimal
                    pass
            elif self._engine_type is libindex.ObjectEngine:
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
        elif needs_i8_conversion(self.dtype):
            # We need to keep M8/m8 dtype when initializing the Engine,
            #  but don't want to change _get_engine_target bc it is used
            #  elsewhere
            # error: Item "ExtensionArray" of "Union[ExtensionArray,
            # ndarray[Any, Any]]" has no attribute "_ndarray"  [union-attr]
            target_values = self._data._ndarray  # type: ignore[union-attr]

        # error: Argument 1 to "ExtensionEngine" has incompatible type
        # "ndarray[Any, Any]"; expected "ExtensionArray"
        return self._engine_type(target_values)  # type: ignore[arg-type]
