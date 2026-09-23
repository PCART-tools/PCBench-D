    def __setstate__(self, state):
        Image.__init__(self)
        info, mode, size, palette, data = state
        self.info = info
        self.mode = mode
        self._size = size
        self.im = core.new(mode, size)
        if mode in ("L", "LA", "P", "PA") and palette:
            self.putpalette(palette)
        self.frombytes(data)
