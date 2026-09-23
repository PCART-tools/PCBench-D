    def __init__(self, fobj, chunk_size=8192):
        self.fobj = fobj
        self.chunk_size = chunk_size
        if hasattr(fobj, 'close'):
            self.close = fobj.close
