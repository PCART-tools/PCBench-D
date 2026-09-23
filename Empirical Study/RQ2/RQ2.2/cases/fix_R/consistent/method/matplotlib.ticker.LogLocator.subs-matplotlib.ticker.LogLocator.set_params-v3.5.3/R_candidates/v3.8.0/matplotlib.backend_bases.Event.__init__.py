    def __init__(self, name, canvas, guiEvent=None):
        self.name = name
        self.canvas = canvas
        self._guiEvent = guiEvent
        self._guiEvent_deleted = False
