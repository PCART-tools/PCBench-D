    @classmethod
    @doc(ExtensionArray._empty)
    def _empty(cls, shape: Shape, dtype: ExtensionDtype):
        values = np.empty(shape, dtype=dtype.type)
        values.fill(cls._internal_fill_value)
        mask = np.ones(shape, dtype=bool)
        result = cls(values, mask)
        if not isinstance(result, cls) or dtype != result.dtype:
            raise NotImplementedError(
                f"Default 'empty' implementation is invalid for dtype='{dtype}'"
            )
        return result
