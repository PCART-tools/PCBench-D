    def _maybe_utc_convert(self: _T, other: Index) -> Tuple[_T, Index]:
        # Overridden by DatetimeIndex
        return self, other
