    def _reduce(
        self, name: str, *, skipna: bool = True, keepdims: bool = False, **kwargs
    ):
        result = super()._reduce(name, skipna=skipna, keepdims=keepdims, **kwargs)
        if name in ["argmax", "argmin"]:
            # don't wrap in Categorical!
            return result
        if keepdims:
            return type(self)(result, dtype=self.dtype)
        else:
            return result
