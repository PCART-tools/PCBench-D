    def __init__(self, figure):
        backend_gtk3.FigureCanvasGTK3.__init__(self, figure)
        self._bbox_queue = []
