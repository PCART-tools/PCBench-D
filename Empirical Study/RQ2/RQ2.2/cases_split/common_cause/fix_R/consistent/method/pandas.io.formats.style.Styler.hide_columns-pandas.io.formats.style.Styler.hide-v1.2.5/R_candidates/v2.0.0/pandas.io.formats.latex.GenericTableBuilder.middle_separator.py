    @property
    def middle_separator(self) -> str:
        return "\\midrule" if self._is_separator_required() else ""
