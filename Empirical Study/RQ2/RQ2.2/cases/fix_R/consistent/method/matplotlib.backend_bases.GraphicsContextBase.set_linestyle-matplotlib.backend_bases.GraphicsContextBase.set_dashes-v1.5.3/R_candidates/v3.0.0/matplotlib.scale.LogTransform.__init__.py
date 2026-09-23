    def __init__(self, base, nonpos='clip'):
        LogTransformBase.__init__(self, nonpos)
        self.base = base
