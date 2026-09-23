    def _set_inaxes(self, inaxes, xy=None):
        self.inaxes = inaxes
        if inaxes is not None:
            try:
                self.xdata, self.ydata = inaxes.transData.inverted().transform(
                    xy if xy is not None else (self.x, self.y))
            except ValueError:
                pass
