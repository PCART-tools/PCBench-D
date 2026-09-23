    def __init__(self, name, canvas, key, x=0, y=0, guiEvent=None):
        self.key = key
        # super-init deferred to the end: callback errors if called before
        super().__init__(name, canvas, x, y, guiEvent=guiEvent)
