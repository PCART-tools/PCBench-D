    def unclosed_group(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        raise ParseFatalException(s, len(s), "Expected '}'")
