    def _call_uncached(
        self, declarations: str | frozenset[tuple[str, str]]
    ) -> dict[str, dict[str, str]]:
        properties = self.compute_css(declarations, self.inherited)
        return self.build_xlstyle(properties)
