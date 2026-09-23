    def view_limits(self, vmin, vmax):
        vmin, vmax = self.base.view_limits(vmin, vmax)
        return mtransforms.nonsingular(min(0, vmin), vmax)
