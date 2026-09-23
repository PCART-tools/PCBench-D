    def __init__(self, figure):
        super(FigureCanvasQTAggBase, self).__init__(figure=figure)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self._agg_draw_pending = False
        self._bbox_queue = []
        self._drawRect = None
