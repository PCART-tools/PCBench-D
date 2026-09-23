    def __init__(self, vocab_file, merges_file, unk_token="<unk>", **kwargs):
        kwargs.setdefault("unk_token", unk_token)
        super().__init__(
            CharBPETokenizer(vocab_file=vocab_file, merges_file=merges_file, unk_token=unk_token, lowercase=True),
            **kwargs,
        )
