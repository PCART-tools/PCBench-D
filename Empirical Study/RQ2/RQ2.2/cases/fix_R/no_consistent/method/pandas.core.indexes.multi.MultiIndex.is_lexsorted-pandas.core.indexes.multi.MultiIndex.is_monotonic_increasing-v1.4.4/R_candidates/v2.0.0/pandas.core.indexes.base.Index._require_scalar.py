    @final
    def _require_scalar(self, value):
        """
        Check that this is a scalar value that we can use for setitem-like
        operations without changing dtype.
        """
        if not is_scalar(value):
            raise TypeError(f"'value' must be a scalar, passed: {type(value).__name__}")
        return value
