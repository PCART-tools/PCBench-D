    @cache_readonly
    def _engine(self) -> IntervalTree:  # type: ignore[override]
        left = self._maybe_convert_i8(self.left)
        right = self._maybe_convert_i8(self.right)
        return IntervalTree(left, right, closed=self.closed)
