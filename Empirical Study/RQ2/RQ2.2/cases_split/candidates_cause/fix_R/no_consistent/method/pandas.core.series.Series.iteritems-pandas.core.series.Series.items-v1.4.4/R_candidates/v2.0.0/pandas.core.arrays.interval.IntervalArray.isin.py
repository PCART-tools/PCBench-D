    def isin(self, values) -> npt.NDArray[np.bool_]:
        if not hasattr(values, "dtype"):
            values = np.array(values)
        values = extract_array(values, extract_numpy=True)

        if is_interval_dtype(values.dtype):
            if self.closed != values.closed:
                # not comparable -> no overlap
                return np.zeros(self.shape, dtype=bool)

            if is_dtype_equal(self.dtype, values.dtype):
                # GH#38353 instead of casting to object, operating on a
                #  complex128 ndarray is much more performant.
                left = self._combined.view("complex128")
                right = values._combined.view("complex128")
                # error: Argument 1 to "in1d" has incompatible type
                # "Union[ExtensionArray, ndarray[Any, Any],
                # ndarray[Any, dtype[Any]]]"; expected
                # "Union[_SupportsArray[dtype[Any]],
                # _NestedSequence[_SupportsArray[dtype[Any]]], bool,
                # int, float, complex, str, bytes, _NestedSequence[
                # Union[bool, int, float, complex, str, bytes]]]"
                return np.in1d(left, right)  # type: ignore[arg-type]

            elif needs_i8_conversion(self.left.dtype) ^ needs_i8_conversion(
                values.left.dtype
            ):
                # not comparable -> no overlap
                return np.zeros(self.shape, dtype=bool)

        return isin(self.astype(object), values.astype(object))
