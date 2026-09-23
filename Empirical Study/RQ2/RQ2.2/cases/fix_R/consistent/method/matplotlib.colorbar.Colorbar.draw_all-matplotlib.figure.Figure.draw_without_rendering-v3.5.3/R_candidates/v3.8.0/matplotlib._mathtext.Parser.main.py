    def main(self, toks: ParseResults) -> list[Hlist]:
        return [Hlist(toks.asList())]
