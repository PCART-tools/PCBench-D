    def __init__(self, *args, orientation, **kwargs):
        self.orientation = orientation
        self._locator = None  # deprecated.
        super().__init__(*args, **kwargs)
