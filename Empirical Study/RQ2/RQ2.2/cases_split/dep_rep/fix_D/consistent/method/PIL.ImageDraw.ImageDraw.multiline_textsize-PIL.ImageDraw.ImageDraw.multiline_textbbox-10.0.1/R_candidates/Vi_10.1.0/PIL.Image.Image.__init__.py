    def __init__(self):
        # FIXME: take "new" parameters / other image?
        # FIXME: turn mode and size into delegating properties?
        self.im = None
        self._mode = ""
        self._size = (0, 0)
        self.palette = None
        self.info = {}
        self.readonly = 0
        self.pyaccess = None
        self._exif = None
