    def _cython_transform(
        self, how: str, numeric_only: bool = True, axis: int = 0, **kwargs
    ):
        raise AbstractMethodError(self)
