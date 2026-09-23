    def __init__(self, name, canvas, mouseevent, artist,
                 guiEvent=None, **kwargs):
        Event.__init__(self, name, canvas, guiEvent)
        self.mouseevent = mouseevent
        self.artist = artist
        self.__dict__.update(kwargs)
