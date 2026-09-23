    def astype(self: T, dtype, copy: bool = False, errors: str = "raise") -> T:
        return self.apply(astype_array_safe, dtype=dtype, copy=copy, errors=errors)
