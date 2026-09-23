    def astype(self, dtype, copy: bool | None = False, errors: str = "raise") -> Self:
        if copy is None:
            copy = True

        return self.apply(astype_array_safe, dtype=dtype, copy=copy, errors=errors)
