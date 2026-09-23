    def apply(
        self: T,
        f,
        align_keys: list[str] | None = None,
        **kwargs,
    ) -> T:
        raise AbstractMethodError(self)
