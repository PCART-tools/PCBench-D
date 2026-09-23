    def _get_engine_target(self) -> ArrayLike:
        """
        Get the ndarray or ExtensionArray that we can pass to the IndexEngine
        constructor.
        """
        vals = self._values
        if isinstance(vals, StringArray):
            # GH#45652 much more performant than ExtensionEngine
            return vals._ndarray
        if isinstance(vals, ArrowExtensionArray) and self.dtype.kind in "Mm":
            import pyarrow as pa

            pa_type = vals._pa_array.type
            if pa.types.is_timestamp(pa_type):
                vals = vals._to_datetimearray()
                return vals._ndarray.view("i8")
            elif pa.types.is_duration(pa_type):
                vals = vals._to_timedeltaarray()
                return vals._ndarray.view("i8")
        if (
            type(self) is Index
            and isinstance(self._values, ExtensionArray)
            and not isinstance(self._values, BaseMaskedArray)
            and not (
                isinstance(self._values, ArrowExtensionArray)
                and is_numeric_dtype(self.dtype)
                # Exclude decimal
                and self.dtype.kind != "O"
            )
        ):
            # TODO(ExtensionIndex): remove special-case, just use self._values
            return self._values.astype(object)
        return vals
