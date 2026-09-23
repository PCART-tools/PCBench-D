    def __next__(self) -> Image.Image:
        try:
            self.im.seek(self.position)
            self.position += 1
            return self.im
        except EOFError as e:
            msg = "end of sequence"
            raise StopIteration(msg) from e
