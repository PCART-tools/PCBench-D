    @classmethod
    def _from_sequence(cls, scalars, *, dtype: Dtype | None = None, copy: bool = False):
        """
        Construct a new ExtensionArray from a sequence of scalars.
        """
        pa_dtype = to_pyarrow_type(dtype)
        if (
            isinstance(scalars, np.ndarray)
            and isinstance(dtype, ArrowDtype)
            and (
                pa.types.is_large_binary(pa_dtype) or pa.types.is_large_string(pa_dtype)
            )
        ):
            # See https://github.com/apache/arrow/issues/35289
            scalars = scalars.tolist()

        if isinstance(scalars, cls):
            scalars = scalars._data
        elif not isinstance(scalars, (pa.Array, pa.ChunkedArray)):
            if copy and is_array_like(scalars):
                # pa array should not get updated when numpy array is updated
                scalars = deepcopy(scalars)
            try:
                scalars = pa.array(scalars, type=pa_dtype, from_pandas=True)
            except pa.ArrowInvalid:
                # GH50430: let pyarrow infer type, then cast
                scalars = pa.array(scalars, from_pandas=True)
        if pa_dtype:
            if pa.types.is_dictionary(pa_dtype):
                scalars = scalars.dictionary_encode()
            else:
                scalars = scalars.cast(pa_dtype)
        arr = cls(scalars)
        if pa.types.is_duration(scalars.type) and scalars.null_count > 0:
            # GH52843: upstream bug for duration types when originally
            # constructed with data containing numpy NaT.
            # https://github.com/apache/arrow/issues/35088
            arr = arr.fillna(arr.dtype.na_value)
        return arr
