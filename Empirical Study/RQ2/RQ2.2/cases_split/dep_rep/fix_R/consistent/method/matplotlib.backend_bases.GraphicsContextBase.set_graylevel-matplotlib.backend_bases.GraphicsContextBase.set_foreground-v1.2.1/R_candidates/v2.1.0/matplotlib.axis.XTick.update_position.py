    def update_position(self, loc):
        'Set the location of tick in data coords with scalar *loc*'
        if self.tick1On:
            self.tick1line.set_xdata((loc,))
        if self.tick2On:
            self.tick2line.set_xdata((loc,))
        if self.gridOn:
            self.gridline.set_xdata((loc,))
        if self.label1On:
            self.label1.set_x(loc)
        if self.label2On:
            self.label2.set_x(loc)

        self._loc = loc
        self.stale = True
