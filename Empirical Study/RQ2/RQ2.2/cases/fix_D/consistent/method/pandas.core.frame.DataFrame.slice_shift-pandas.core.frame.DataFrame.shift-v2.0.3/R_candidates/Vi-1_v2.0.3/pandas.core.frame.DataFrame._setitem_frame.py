    def _setitem_frame(self, key, value):
        # support boolean setting with DataFrame input, e.g.
        # df[df > df2] = 0
        if isinstance(key, np.ndarray):
            if key.shape != self.shape:
                raise ValueError("Array conditional must be same shape as self")
            key = self._constructor(key, **self._construct_axes_dict(), copy=False)

        if key.size and not all(is_bool_dtype(dtype) for dtype in key.dtypes):
            raise TypeError(
                "Must pass DataFrame or 2-d ndarray with boolean values only"
            )

        self._check_inplace_setting(value)
        self._check_setitem_copy()
        self._where(-key, value, inplace=True)
