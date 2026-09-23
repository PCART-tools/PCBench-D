    def astype(self, dtype, copy: bool = False, errors: str = "raise"):
        return self.apply("astype", dtype=dtype, copy=copy, errors=errors)
