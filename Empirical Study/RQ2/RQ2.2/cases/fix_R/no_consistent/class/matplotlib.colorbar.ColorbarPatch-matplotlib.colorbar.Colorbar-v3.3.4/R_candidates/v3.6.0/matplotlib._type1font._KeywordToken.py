class _KeywordToken(_Token):
    kind = 'keyword'

    def is_keyword(self, *names):
        return self.raw in names
