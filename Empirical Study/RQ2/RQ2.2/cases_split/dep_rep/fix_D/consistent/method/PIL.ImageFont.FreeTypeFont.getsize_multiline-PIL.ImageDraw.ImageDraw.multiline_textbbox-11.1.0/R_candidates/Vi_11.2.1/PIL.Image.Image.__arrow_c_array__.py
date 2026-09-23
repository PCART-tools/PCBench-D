    def __arrow_c_array__(
        self, requested_schema: object | None = None
    ) -> tuple[object, object]:
        self.load()
        return (self.im.__arrow_c_schema__(), self.im.__arrow_c_array__())
