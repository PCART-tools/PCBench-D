    def __init__(self, model: str):
        requires_sentencepiece(self)
        from sentencepiece import SentencePieceProcessor

        self.sp = SentencePieceProcessor()
        self.sp.Load(model)
