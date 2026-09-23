    def _reduce(
        self, name: str, *, skipna: bool = True, keepdims: bool = False, **kwargs
    ):
        if name in ["any", "all"]:
            arr = pc.and_kleene(
                pc.invert(pc.is_null(self._pa_array)), pc.not_equal(self._pa_array, "")
            )
            return ArrowExtensionArray(arr)._reduce(
                name, skipna=skipna, keepdims=keepdims, **kwargs
            )
        else:
            return super()._reduce(name, skipna=skipna, keepdims=keepdims, **kwargs)
