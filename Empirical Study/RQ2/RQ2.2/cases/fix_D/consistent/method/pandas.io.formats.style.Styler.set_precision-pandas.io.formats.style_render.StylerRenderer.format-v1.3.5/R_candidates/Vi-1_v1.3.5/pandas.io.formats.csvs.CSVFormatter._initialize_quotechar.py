    def _initialize_quotechar(self, quotechar: str | None) -> str | None:
        if self.quoting != csvlib.QUOTE_NONE:
            # prevents crash in _csv
            return quotechar
        return None
