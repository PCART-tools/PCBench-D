    def __next__(self):
        data = self.fobj.read(self.chunk_size)
        if data:
            return data
        raise StopIteration
