    def __init__(self, nonpos='mask'):
        Transform.__init__(self)
        self._nonpos = nonpos
        self._clip = {"clip": True, "mask": False}[nonpos]
