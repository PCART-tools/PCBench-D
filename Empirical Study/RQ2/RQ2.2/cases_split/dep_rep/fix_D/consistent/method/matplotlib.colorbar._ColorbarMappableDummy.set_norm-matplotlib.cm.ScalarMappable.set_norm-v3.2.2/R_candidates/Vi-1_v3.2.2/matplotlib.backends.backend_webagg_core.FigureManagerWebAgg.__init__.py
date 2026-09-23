    def __init__(self, canvas, num):
        backend_bases.FigureManagerBase.__init__(self, canvas, num)

        self.web_sockets = set()

        self.toolbar = self._get_toolbar(canvas)
