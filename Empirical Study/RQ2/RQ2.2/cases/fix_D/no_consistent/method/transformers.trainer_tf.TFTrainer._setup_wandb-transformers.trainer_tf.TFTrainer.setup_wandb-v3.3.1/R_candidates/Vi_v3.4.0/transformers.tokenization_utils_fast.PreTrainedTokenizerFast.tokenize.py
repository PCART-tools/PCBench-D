    def tokenize(self, text: str, pair: Optional[str] = None, add_special_tokens: bool = False) -> List[str]:
        """
        Converts a string in a sequence of tokens, using the backend Rust tokenizer.

        Note that, unlike slow tokenizers (instances of :class:`~transformers.PreTrainedTokenizer`), this method
        will replace the unknown tokens with the :obj:`unk_token`.

        Args:
            text (:obj:`str`):
                The sequence to be encoded.
            pair (:obj:`str`, `optional`):
                A second sequence to be encoded with the first.
            add_special_tokens (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not to add the special tokens associated with the corresponding model.

        Returns:
            :obj:`List[str]`: The list of tokens.
        """
        return self._tokenizer.encode(text, pair, add_special_tokens=add_special_tokens).tokens
