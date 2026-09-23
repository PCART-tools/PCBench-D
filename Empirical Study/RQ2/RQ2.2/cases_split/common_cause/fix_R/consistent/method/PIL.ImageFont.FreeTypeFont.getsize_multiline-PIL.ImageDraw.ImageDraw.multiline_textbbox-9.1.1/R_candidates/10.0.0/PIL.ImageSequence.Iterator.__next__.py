    def __next__(self):
        try:
            self.im.seek(self.position)
            self.position += 1
            return self.im
        except EOFError as e:
            raise StopIteration from e
