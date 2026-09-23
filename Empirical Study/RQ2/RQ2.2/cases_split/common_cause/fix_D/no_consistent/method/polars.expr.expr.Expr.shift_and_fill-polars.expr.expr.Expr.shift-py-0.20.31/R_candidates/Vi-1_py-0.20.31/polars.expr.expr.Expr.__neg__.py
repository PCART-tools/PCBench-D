    def __neg__(self) -> Self:
        return self._from_pyexpr(-self._pyexpr)
