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
        # clearing the axes will delete outline, patch, solids, and lines:
        self.outline = None
        self.patch = None
        self.solids = None
        self.lines = list()
        self.dividers = None
        self.set_alpha(mappable.get_alpha())
        self.cmap = mappable.cmap
        self.norm = mappable.norm
        self.config_axis()
        self.draw_all()
        if isinstance(self.mappable, contour.ContourSet):
            CS = self.mappable
            if not CS.filled:
                self.add_lines(CS)
