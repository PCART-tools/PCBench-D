    def __getitem__(self, ix: int) -> Image.Image:
        try:
            self.im.seek(ix)
            return self.im
        except EOFError as e:
            msg = "end of sequence"
            raise IndexError(msg) from e
