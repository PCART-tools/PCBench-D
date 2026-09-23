    def __init__(self, nonpos='clip'):
        Transform.__init__(self)
        self._clip = {"clip": True, "mask": False}[nonpos]
