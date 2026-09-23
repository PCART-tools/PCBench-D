    def __new__(
        cls,
        value: int | None = None,
        name: str = "unknown",
        type: int | None = None,
        length: int | None = None,
        enum: dict[str, int] | None = None,
    ) -> TagInfo:
        return super().__new__(cls, value, name, type, length, enum or {})
