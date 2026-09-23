    def update_normal(self, mappable):
        '''
        update solid, lines, etc. Unlike update_bruteforce, it does
        not clear the axes.  This is meant to be called when the image
        or contour plot to which this colorbar belongs is changed.
        '''
        self.draw_all()
        if isinstance(self.mappable, contour.ContourSet):
            CS = self.mappable
            if not CS.filled:
                self.add_lines(CS)
        self.stale = True
