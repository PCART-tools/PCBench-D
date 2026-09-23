    @cache_readonly
    def _multiindex(self) -> MultiIndex:
        return MultiIndex.from_arrays([self.left, self.right], names=["left", "right"])
