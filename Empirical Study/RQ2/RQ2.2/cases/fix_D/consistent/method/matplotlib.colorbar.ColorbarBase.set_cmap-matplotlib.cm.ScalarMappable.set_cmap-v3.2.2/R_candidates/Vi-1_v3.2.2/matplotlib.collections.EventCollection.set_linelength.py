    def set_linelength(self, linelength):
        '''
        set the length of the lines used to mark each event
        '''
        if linelength == self.get_linelength():
            return
        lineoffset = self.get_lineoffset()
        segments = self.get_segments()
        pos = 1 if self.is_horizontal() else 0
        for segment in segments:
            segment[0, pos] = lineoffset + linelength / 2.
            segment[1, pos] = lineoffset - linelength / 2.
        self.set_segments(segments)
        self._linelength = linelength
