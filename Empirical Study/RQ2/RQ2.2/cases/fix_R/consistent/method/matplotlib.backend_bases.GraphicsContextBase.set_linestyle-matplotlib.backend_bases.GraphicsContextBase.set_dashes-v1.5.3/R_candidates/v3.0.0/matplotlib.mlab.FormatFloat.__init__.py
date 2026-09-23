    def __init__(self, precision=4, scale=1.):
        FormatFormatStr.__init__(self, '%%1.%df' % precision)
        self.precision = precision
        self.scale = scale
