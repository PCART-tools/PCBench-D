    def _tokenize(self, text):
        """ Tokenize a string. """
        split_tokens = []
        if self.fix_text is None:
            # Using BERT's BasicTokenizer
            text = self.nlp.tokenize(text)
            for token in text:
                split_tokens.extend([t for t in self.bpe(token).split(" ")])
        else:
            # Using SpaCy & ftfy (original tokenization process of OpenAI GPT)
            text = self.nlp(text_standardize(self.fix_text(text)))
            for token in text:
                split_tokens.extend([t for t in self.bpe(token.text.lower()).split(" ")])
        return split_tokens
