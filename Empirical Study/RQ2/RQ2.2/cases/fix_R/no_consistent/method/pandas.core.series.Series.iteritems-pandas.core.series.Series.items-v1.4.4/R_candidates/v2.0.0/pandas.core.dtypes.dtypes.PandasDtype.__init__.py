    def __init__(self, dtype: npt.DTypeLike | PandasDtype | None) -> None:
        if isinstance(dtype, PandasDtype):
            # make constructor univalent
            dtype = dtype.numpy_dtype
        self._dtype = np.dtype(dtype)
