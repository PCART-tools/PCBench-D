    def __init__(self, *args):
        super().__init__(*args)
        self.proto = get_proto(self.original_tokenizer.vocab_file)
