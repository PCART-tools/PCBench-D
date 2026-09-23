    def __init__(self, marker_pad=0.3, numpoints=None,
                 bottom=None, yoffsets=None, **kw):

        HandlerNpointsYoffsets.__init__(self, marker_pad=marker_pad,
                                        numpoints=numpoints,
                                        yoffsets=yoffsets,
                                        **kw)
        self._bottom = bottom
