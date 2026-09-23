    def __init__(self, nonpos='mask'):
        Transform.__init__(self)
        cbook._check_in_list(['mask', 'clip'], nonpos=nonpos)
        self._nonpos = nonpos
        self._clip = {"clip": True, "mask": False}[nonpos]
