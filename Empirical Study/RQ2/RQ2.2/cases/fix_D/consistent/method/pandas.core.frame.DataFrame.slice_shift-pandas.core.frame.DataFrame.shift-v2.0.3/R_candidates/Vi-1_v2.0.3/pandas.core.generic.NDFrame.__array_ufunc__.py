    @final
    def __array_ufunc__(
        self, ufunc: np.ufunc, method: str, *inputs: Any, **kwargs: Any
    ):
        return arraylike.array_ufunc(self, ufunc, method, *inputs, **kwargs)
