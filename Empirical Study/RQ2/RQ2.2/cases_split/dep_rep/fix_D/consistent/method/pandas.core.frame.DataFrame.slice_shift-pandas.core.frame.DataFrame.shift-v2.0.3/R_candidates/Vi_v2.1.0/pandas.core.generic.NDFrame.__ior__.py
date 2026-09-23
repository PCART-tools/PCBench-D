    @final
    def __ior__(self, other) -> Self:
        return self._inplace_method(other, type(self).__or__)
