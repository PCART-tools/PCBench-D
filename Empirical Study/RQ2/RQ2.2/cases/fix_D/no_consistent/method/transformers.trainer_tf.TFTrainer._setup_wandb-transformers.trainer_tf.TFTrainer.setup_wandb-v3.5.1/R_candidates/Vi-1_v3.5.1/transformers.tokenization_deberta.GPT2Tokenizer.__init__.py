    def __init__(self, vocab_file=None, special_tokens=None):
        self.pad_token = "[PAD]"
        self.sep_token = "[SEP]"
        self.unk_token = "[UNK]"
        self.cls_token = "[CLS]"

        self.symbols = []
        self.count = []
        self.indices = {}
        self.pad_token_id = self.add_symbol(self.pad_token)
        self.cls_token_id = self.add_symbol(self.cls_token)
        self.sep_token_id = self.add_symbol(self.sep_token)
        self.unk_token_id = self.add_symbol(self.unk_token)

        self.gpt2_encoder = load_vocab(vocab_file)
        self.bpe = get_encoder(self.gpt2_encoder["encoder"], self.gpt2_encoder["vocab"])
        for w, n in self.gpt2_encoder["dict_map"]:
            self.add_symbol(w, n)

        self.mask_token = "[MASK]"
        self.mask_id = self.add_symbol(self.mask_token)
        self.special_tokens = ["[MASK]", "[SEP]", "[PAD]", "[UNK]", "[CLS]"]
        if special_tokens is not None:
            for t in special_tokens:
                self.add_special_token(t)

        self.vocab = self.indices
        self.ids_to_tokens = self.symbols
