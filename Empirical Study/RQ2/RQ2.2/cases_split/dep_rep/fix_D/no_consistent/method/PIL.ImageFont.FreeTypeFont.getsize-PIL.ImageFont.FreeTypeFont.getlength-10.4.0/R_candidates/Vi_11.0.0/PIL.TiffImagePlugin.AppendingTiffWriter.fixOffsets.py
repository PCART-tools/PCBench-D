    def fixOffsets(
        self, count: int, isShort: bool = False, isLong: bool = False
    ) -> None:
        if isShort:
            field_size = 2
        elif isLong:
            field_size = 4
        else:
            field_size = 0
        return self._fixOffsets(count, field_size)
