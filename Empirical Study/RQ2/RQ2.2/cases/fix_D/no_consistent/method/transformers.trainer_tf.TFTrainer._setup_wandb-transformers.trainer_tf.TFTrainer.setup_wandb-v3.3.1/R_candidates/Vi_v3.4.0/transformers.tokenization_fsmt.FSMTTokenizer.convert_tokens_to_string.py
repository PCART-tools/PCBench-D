    def convert_tokens_to_string(self, tokens):
        """ Converts a sequence of tokens (string) in a single string. """

        # remove BPE
        tokens = [t.replace(" ", "").replace("</w>", " ") for t in tokens]
        tokens = "".join(tokens).split()
        # detokenize
        text = self.moses_detokenize(tokens, self.tgt_lang)
        return text
