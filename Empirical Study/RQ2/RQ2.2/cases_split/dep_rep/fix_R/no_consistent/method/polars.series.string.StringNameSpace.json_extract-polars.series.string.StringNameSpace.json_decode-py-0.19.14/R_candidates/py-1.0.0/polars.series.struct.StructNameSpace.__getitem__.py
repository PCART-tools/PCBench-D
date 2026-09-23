    def __getitem__(self, item: int | str) -> Series:
        if isinstance(item, int):
            return self.field(self.fields[item])
        elif isinstance(item, str):
            return self.field(item)
        else:
            msg = f"expected type 'int | str', got {type(item).__name__!r}"
            raise TypeError(msg)
