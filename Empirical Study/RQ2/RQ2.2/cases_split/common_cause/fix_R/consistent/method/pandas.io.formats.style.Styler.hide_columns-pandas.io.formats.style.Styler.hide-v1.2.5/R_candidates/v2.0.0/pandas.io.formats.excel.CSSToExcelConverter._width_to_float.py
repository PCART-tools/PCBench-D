    def _width_to_float(self, width: str | None) -> float:
        if width is None:
            width = "2pt"
        return self._pt_to_float(width)
