    def unknown_symbol(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        raise ParseFatalException(s, loc, f"Unknown symbol: {toks['name']}")
