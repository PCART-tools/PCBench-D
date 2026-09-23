    def _multiline_split(self, text) -> list[str | bytes]:
        split_character = "\n" if isinstance(text, str) else b"\n"

        return text.split(split_character)
