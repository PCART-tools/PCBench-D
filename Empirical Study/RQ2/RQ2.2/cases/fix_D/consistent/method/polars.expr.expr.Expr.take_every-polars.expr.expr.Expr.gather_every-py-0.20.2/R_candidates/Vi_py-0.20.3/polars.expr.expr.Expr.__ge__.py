    def __ge__(self, other: Any) -> Self:
        _warn_null_comparison(other)
        return self._from_pyexpr(self._pyexpr.gt_eq(self._to_pyexpr(other)))
