    def update_bruteforce(self, mappable):
        '''
        Destroy and rebuild the colorbar.  This is
        intended to become obsolete, and will probably be
        deprecated and then removed.  It is not called when
        the pyplot.colorbar function or the Figure.colorbar
        method are used to create the colorbar.

        '''
        # We are using an ugly brute-force method: clearing and
        # redrawing the whole thing.  The problem is that if any
        # properties have been changed by methods other than the
        # colorbar methods, those changes will be lost.
        self.ax.cla()
        self.locator = None
        self.formatter = None

        # clearing the axes will delete outline, patch, solids, and lines:
        self.outline = None
        self.patch = None
        self.solids = None
        self.lines = list()
        self.dividers = None
        self.update_normal(mappable)
        self.draw_all()
        if isinstance(self.mappable, contour.ContourSet):
            CS = self.mappable
            if not CS.filled:
                self.add_lines(CS)
