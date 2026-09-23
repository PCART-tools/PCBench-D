    def _cython_transform(
        self, how: str, numeric_only: bool = False, axis: AxisInt = 0, **kwargs
    ):
        raise AbstractMethodError(self)
