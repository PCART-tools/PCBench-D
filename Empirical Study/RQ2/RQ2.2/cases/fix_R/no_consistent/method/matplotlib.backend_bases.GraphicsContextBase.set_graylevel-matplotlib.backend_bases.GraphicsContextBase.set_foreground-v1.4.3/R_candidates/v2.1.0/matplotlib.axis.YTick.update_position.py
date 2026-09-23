    def update_position(self, loc):
        'Set the location of tick in data coords with scalar *loc*'
        if self.tick1On:
            self.tick1line.set_ydata((loc,))
        if self.tick2On:
            self.tick2line.set_ydata((loc,))
        if self.gridOn:
            self.gridline.set_ydata((loc,))
        if self.label1On:
            self.label1.set_y(loc)
        if self.label2On:
            self.label2.set_y(loc)

        self._loc = loc
        self.stale = True
