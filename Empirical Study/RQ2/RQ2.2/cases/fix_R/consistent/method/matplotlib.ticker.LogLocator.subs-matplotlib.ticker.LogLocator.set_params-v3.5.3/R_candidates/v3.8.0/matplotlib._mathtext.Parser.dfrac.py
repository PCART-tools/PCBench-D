    def dfrac(self, toks: ParseResults) -> T.Any:
        return self._genfrac(
            "", "", self.get_state().get_current_underline_thickness(),
            self._MathStyle.DISPLAYSTYLE, toks["num"], toks["den"])
