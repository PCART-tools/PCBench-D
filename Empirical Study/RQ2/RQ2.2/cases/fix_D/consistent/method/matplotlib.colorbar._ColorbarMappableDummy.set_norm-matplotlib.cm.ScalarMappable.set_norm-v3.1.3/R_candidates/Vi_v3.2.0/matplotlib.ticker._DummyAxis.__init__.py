    def __init__(self, minpos=0):
        self.dataLim = mtransforms.Bbox.unit()
        self.viewLim = mtransforms.Bbox.unit()
        self._minpos = minpos
