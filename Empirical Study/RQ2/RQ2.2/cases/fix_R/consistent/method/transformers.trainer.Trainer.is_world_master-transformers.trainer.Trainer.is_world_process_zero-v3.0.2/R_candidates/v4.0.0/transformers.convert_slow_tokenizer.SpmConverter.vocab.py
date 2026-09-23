    def vocab(self, proto):
        return [(piece.piece, piece.score) for piece in proto.pieces]
