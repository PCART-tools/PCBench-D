    def chunk_IEND(self, pos: int, length: int) -> NoReturn:
        msg = "end of PNG image"
        raise EOFError(msg)
