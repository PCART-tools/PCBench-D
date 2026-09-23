    def chunk_IEND(self, pos, length):
        msg = "end of PNG image"
        raise EOFError(msg)
