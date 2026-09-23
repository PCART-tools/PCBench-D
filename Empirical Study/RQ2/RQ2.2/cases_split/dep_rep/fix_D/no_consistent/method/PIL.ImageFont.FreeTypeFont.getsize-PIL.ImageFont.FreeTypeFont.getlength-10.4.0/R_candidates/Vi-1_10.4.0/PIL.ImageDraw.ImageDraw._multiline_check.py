    def _multiline_check(self, text: AnyStr) -> bool:
        split_character = "\n" if isinstance(text, str) else b"\n"

        return split_character in text
