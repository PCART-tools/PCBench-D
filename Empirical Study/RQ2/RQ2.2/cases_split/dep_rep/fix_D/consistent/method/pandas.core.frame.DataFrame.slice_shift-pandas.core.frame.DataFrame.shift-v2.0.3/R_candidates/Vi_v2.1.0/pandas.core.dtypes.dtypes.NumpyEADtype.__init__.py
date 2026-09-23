    def __init__(self, dtype: npt.DTypeLike | NumpyEADtype | None) -> None:
        if isinstance(dtype, NumpyEADtype):
            # make constructor univalent
            dtype = dtype.numpy_dtype
        self._dtype = np.dtype(dtype)
