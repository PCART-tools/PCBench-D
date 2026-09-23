    def __init__(self, marker_pad=0.3, numpoints=None, **kw):
        HandlerBase.__init__(self, **kw)

        self._numpoints = numpoints
        self._marker_pad = marker_pad
