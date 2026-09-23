    def __rand__(self, other: Series) -> Series:
        if not isinstance(other, Series):
            other = Series([other])
        return other & self
