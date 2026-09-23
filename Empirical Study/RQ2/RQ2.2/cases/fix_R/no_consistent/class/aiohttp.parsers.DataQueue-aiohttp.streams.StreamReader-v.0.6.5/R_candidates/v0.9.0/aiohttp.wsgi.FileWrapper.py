class FileWrapper:
    """Custom file wrapper."""

    def __init__(self, fobj, chunk_size=8192):
        self.fobj = fobj
        self.chunk_size = chunk_size
        if hasattr(fobj, 'close'):
            self.close = fobj.close

    def __iter__(self):
        return self

    def __next__(self):
        data = self.fobj.read(self.chunk_size)
        if data:
            return data
        raise StopIteration
