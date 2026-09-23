    def __str__(self):
        return "Annotation(%g,%g,%s)" % (self.xy[0],
                                         self.xy[1],
                                         repr(self._text))
