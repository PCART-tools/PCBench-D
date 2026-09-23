    def __ge__(self, other: Any) -> Self:
        return self._from_pyexpr(self._pyexpr.gt_eq(self._to_pyexpr(other)))
