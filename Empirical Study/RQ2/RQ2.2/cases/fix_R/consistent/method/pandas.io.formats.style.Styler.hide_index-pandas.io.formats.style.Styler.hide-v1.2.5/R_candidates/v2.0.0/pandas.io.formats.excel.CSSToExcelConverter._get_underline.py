    def _get_underline(self, decoration: Sequence[str]) -> str | None:
        if "underline" in decoration:
            return "single"
        return None
