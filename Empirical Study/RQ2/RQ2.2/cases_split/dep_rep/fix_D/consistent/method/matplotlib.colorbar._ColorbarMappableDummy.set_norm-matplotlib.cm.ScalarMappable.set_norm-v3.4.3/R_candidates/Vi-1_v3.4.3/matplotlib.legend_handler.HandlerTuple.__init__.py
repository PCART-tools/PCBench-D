    def __init__(self, ndivide=1, pad=None, **kwargs):
        self._ndivide = ndivide
        self._pad = pad
        super().__init__(**kwargs)
