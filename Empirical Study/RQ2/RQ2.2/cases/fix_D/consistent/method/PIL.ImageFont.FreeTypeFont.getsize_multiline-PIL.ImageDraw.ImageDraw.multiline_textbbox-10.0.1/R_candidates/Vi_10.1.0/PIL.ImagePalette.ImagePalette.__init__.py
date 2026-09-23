    def __init__(self, mode="RGB", palette=None):
        self.mode = mode
        self.rawmode = None  # if set, palette contains raw data
        self.palette = palette or bytearray()
        self.dirty = None
