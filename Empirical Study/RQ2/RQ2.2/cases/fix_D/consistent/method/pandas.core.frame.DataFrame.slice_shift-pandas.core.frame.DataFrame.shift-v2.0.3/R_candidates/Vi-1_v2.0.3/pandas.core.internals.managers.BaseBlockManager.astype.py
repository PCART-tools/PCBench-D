    def astype(self: T, dtype, copy: bool | None = False, errors: str = "raise") -> T:
        if copy is None:
            if using_copy_on_write():
                copy = False
            else:
                copy = True
        elif using_copy_on_write():
            copy = False

        return self.apply(
            "astype",
            dtype=dtype,
            copy=copy,
            errors=errors,
            using_cow=using_copy_on_write(),
        )
