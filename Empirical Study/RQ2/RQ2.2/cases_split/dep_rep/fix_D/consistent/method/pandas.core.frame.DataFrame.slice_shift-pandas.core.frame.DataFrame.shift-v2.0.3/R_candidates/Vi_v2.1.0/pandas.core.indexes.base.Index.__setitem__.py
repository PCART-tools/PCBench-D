    @final
    def __setitem__(self, key, value) -> None:
        raise TypeError("Index does not support mutable operations")
