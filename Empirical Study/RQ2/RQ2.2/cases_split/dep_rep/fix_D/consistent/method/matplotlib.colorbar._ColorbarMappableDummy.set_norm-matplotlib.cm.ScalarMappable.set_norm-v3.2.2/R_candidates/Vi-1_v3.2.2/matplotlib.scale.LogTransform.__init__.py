    def __init__(self, base, nonpos='clip'):
        Transform.__init__(self)
        self.base = base
        self._clip = {"clip": True, "mask": False}[nonpos]
