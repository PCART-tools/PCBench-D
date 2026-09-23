    def __init__(self, center, viewLim, originLim, **kwargs):
        mtransforms.Bbox.__init__(self,
                                  np.array([[0.0, 0.0], [1.0, 1.0]], np.float),
                                  **kwargs)
        self._center = center
        self._viewLim = viewLim
        self._originLim = originLim
        self.set_children(viewLim, originLim)
