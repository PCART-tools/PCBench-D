    def __init__(self, canvas, num):
        self.web_sockets = set()
        super().__init__(canvas, num)
        self.toolbar = self._get_toolbar(canvas)
