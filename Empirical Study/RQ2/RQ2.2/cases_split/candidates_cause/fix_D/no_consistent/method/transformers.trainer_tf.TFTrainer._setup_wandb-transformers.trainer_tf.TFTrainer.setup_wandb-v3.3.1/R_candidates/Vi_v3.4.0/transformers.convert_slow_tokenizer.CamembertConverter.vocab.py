    def vocab(self, proto):
        vocab = [
            ("<s>NOTUSED", 0.0),
            ("<pad>", 0.0),
            ("</s>NOTUSED", 0.0),
            ("<unk>", 0.0),
        ]
        # We down-grade the original SentencePiece by -100 to avoid using it and use our added token instead
        vocab += [(piece.piece, piece.score if i != 0 else piece.score - 100) for i, piece in enumerate(proto.pieces)]
        vocab += [("<mask>", 0.0)]
        return vocab
