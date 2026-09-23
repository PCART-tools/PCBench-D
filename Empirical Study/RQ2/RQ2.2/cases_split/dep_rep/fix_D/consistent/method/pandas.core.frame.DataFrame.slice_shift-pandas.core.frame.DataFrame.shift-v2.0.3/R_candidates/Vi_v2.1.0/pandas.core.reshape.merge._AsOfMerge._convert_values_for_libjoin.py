    def _convert_values_for_libjoin(
        self, values: AnyArrayLike, side: str
    ) -> np.ndarray:
        # we require sortedness and non-null values in the join keys
        if not Index(values).is_monotonic_increasing:
            if isna(values).any():
                raise ValueError(f"Merge keys contain null values on {side} side")
            raise ValueError(f"{side} keys must be sorted")

        if isinstance(values, ArrowExtensionArray):
            values = values._maybe_convert_datelike_array()

        if needs_i8_conversion(values.dtype):
            values = values.view("i8")

        elif isinstance(values, BaseMaskedArray):
            # we've verified above that no nulls exist
            values = values._data
        elif isinstance(values, ExtensionArray):
            values = values.to_numpy()

        # error: Incompatible return value type (got "Union[ExtensionArray,
        # Any, ndarray[Any, Any], ndarray[Any, dtype[Any]], Index, Series]",
        # expected "ndarray[Any, Any]")
        return values  # type: ignore[return-value]
