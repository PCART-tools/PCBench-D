    def __array_ufunc__(self, ufunc: np.ufunc, method: str, *inputs, **kwargs):
        if (
            ufunc in [np.isnan, np.isinf, np.isfinite]
            and len(inputs) == 1
            and inputs[0] is self
        ):
            # numpy 1.18 changed isinf and isnan to not raise on dt64/td64
            return getattr(ufunc, method)(self._ndarray, **kwargs)

        return super().__array_ufunc__(ufunc, method, *inputs, **kwargs)
