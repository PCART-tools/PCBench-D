    def vocab(self, proto):
        vocab = [
            (self.original_tokenizer.pad_token, 0),
            (self.original_tokenizer.eos_token, 0),
        ]
        vocab += [(f"unk_{i}", -100) for i in range(2, 2 + self.original_tokenizer.offset)]
        vocab += [(piece.piece, piece.score) for piece in proto.pieces[2:]]
        return vocab
