    @property
    def _position_macro(self) -> str:
        r"""Position macro, extracted from self.position, like [h]."""
        return f"[{self.position}]" if self.position else ""
