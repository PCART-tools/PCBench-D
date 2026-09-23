    def pan(self, numsteps):
        """Pan numticks (can be positive or negative)"""
        ticks = self()
        numticks = len(ticks)

        vmin, vmax = self.axis.get_view_interval()
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        if numticks > 2:
            step = numsteps * abs(ticks[0] - ticks[1])
        else:
            d = abs(vmax - vmin)
            step = numsteps * d / 6.

        vmin += step
        vmax += step
        self.axis.set_view_interval(vmin, vmax, ignore=True)
