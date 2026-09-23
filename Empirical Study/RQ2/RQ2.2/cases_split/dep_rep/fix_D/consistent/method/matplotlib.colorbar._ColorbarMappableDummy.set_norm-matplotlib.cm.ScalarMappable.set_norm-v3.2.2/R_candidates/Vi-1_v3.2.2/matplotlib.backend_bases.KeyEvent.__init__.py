    def __init__(self, name, canvas, key, x=0, y=0, guiEvent=None):
        self.key = key
        # super-init deferred to the end: callback errors if called before
        LocationEvent.__init__(self, name, canvas, x, y, guiEvent=guiEvent)
