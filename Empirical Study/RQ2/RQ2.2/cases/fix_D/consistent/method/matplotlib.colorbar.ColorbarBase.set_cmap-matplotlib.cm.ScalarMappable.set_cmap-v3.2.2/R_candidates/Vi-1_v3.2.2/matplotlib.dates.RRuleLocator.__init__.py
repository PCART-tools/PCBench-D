    def __init__(self, o, tz=None):
        DateLocator.__init__(self, tz)
        self.rule = o
