    def space(self, toks: ParseResults) -> T.Any:
        num = self._space_widths[toks["space"]]
        box = self._make_space(num)
        return [box]
