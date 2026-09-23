    def __repr__(self) -> str:
        if len(expr_str := self._pyexpr.to_str()) > 30:
            expr_str = f"{expr_str[:30]}…"
        return f"<{self.__class__.__name__} [{expr_str!r}] at 0x{id(self):X}>"
