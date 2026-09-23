    def __init__(self, parent, *args, **kwargs):
        self._timer = None
        super().__init__(*args, **kwargs)
        self.parent = parent
