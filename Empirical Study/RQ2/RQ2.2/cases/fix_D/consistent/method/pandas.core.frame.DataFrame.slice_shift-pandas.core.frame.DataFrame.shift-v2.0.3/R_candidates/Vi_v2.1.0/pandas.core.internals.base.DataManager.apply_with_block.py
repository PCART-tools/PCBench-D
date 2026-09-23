    def apply_with_block(
        self,
        f,
        align_keys: list[str] | None = None,
        **kwargs,
    ) -> Self:
        raise AbstractMethodError(self)
