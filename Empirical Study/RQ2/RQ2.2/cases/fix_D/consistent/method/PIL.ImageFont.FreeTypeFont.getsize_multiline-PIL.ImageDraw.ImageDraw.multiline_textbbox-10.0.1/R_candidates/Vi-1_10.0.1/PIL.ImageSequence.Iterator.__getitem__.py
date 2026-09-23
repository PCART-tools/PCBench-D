    def __getitem__(self, ix):
        try:
            self.im.seek(ix)
            return self.im
        except EOFError as e:
            raise IndexError from e  # end of sequence
