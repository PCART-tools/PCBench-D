    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dont use reserved words added_token_encoder, added_tokens_decoder because of
        # AssertionError: Non-consecutive added token '1' found. in from_pretrained
        assert len(self.added_tokens_decoder) == 0
        self.encoder: Dict[int, str] = {0: self.pad_token, 1: self.eos_token}
        # entries 2-104 are only used for pretraining and called unk_2, ...unk_104
        self.encoder.update({i: f"unk_{i}" for i in range(2, self.offset + 2)})
        self.decoder: Dict[str, int] = {v: k for k, v in self.encoder.items()}
