    @cbook.deprecated("3.3")
    def zoom(self, direction):
        """Zoom in/out on axis; if direction is >0 zoom in, else zoom out."""

        vmin, vmax = self.axis.get_view_interval()
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        interval = abs(vmax - vmin)
        step = 0.1 * interval * direction
        self.axis.set_view_interval(vmin + step, vmax - step, ignore=True)
