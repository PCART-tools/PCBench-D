    def __init__(self, minpos=0):
        self._dataLim = mtransforms.Bbox.unit()
        self._viewLim = mtransforms.Bbox.unit()
        self._minpos = minpos
