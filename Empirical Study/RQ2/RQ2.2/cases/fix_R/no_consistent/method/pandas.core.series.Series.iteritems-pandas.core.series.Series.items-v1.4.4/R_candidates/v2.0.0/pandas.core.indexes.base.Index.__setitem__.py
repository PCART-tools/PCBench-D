    @final
    def __setitem__(self, key, value):
        raise TypeError("Index does not support mutable operations")
