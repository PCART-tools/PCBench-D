    def tokenize(self, text, never_split=None, **kwargs):
        """Tokenizes a piece of text."""
        if self.normalize_text:
            text = unicodedata.normalize("NFKC", text)

        never_split = self.never_split + (never_split if never_split is not None else [])
        tokens = []

        for word in self.mecab(text):
            token = word.surface

            if self.do_lower_case and token not in never_split:
                token = token.lower()

            tokens.append(token)

        return tokens
