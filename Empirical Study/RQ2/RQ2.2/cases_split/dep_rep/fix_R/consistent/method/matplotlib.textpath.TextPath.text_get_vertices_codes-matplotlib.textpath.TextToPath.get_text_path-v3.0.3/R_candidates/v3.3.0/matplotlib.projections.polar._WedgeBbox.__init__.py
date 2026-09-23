    def __init__(self, center, viewLim, originLim, **kwargs):
        mtransforms.Bbox.__init__(self, [[0, 0], [1, 1]], **kwargs)
        self._center = center
        self._viewLim = viewLim
        self._originLim = originLim
        self.set_children(viewLim, originLim)
