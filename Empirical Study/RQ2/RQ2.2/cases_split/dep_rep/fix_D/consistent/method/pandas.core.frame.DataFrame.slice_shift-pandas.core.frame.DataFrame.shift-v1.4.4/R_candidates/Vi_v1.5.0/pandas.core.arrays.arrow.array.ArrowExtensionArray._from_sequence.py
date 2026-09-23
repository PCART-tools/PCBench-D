    @classmethod
    def _from_sequence(cls, scalars, *, dtype: Dtype | None = None, copy=False):
        """
        Construct a new ExtensionArray from a sequence of scalars.
        """
        pa_dtype = to_pyarrow_type(dtype)
        is_cls = isinstance(scalars, cls)
        if is_cls or isinstance(scalars, (pa.Array, pa.ChunkedArray)):
            if is_cls:
                scalars = scalars._data
            if pa_dtype:
                scalars = scalars.cast(pa_dtype)
            return cls(scalars)
        else:
            return cls(
                pa.chunked_array(pa.array(scalars, type=pa_dtype, from_pandas=True))
            )
