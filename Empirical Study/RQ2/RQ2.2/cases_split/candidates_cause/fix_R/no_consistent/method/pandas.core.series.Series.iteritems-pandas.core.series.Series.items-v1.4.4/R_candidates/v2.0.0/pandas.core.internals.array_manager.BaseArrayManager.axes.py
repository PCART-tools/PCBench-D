    @property
    # error: Signature of "axes" incompatible with supertype "DataManager"
    def axes(self) -> list[Index]:  # type: ignore[override]
        # mypy doesn't work to override attribute with property
        # see https://github.com/python/mypy/issues/4125
        """Axes is BlockManager-compatible order (columns, rows)"""
        return [self._axes[1], self._axes[0]]
