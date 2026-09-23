    def __init__(self, name, canvas, mouseevent, artist,
                 guiEvent=None, **kwargs):
        super().__init__(name, canvas, guiEvent)
        self.mouseevent = mouseevent
        self.artist = artist
        self.__dict__.update(kwargs)
