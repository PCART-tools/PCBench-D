    def __rand__(self, other: Any) -> Series:
        if not isinstance(other, Series):
            other = Series([other])
        return other & self
