    def __init__(self, tokenizer: BaseTokenizerFast, **kwargs):
        if not isinstance(tokenizer, BaseTokenizerFast):
            raise ValueError(
                "Tokenizer should be an instance of a BaseTokenizer " "provided by HuggingFace tokenizers library."
            )
        self._tokenizer: BaseTokenizerFast = tokenizer

        # We call this after having initialized the backend tokenizer because we update it.
        super().__init__(**kwargs)
