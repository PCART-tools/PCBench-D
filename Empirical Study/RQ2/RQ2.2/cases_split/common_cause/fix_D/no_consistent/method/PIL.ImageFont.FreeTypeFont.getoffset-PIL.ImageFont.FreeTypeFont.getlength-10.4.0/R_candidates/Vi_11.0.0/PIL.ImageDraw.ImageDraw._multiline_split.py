    def _multiline_split(self, text: AnyStr) -> list[AnyStr]:
        return text.split("\n" if isinstance(text, str) else b"\n")
