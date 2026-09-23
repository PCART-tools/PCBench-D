    @_api.deprecated("3.7",
                     addendum="Any custom property styling may be lost.")
    @property
    def lines(self):
        if not hasattr(self, "_lines"):
            ys = np.linspace(1, 0, len(self.labels)+2)[1:-1]
            self._checks.set_visible(False)
            dy = 1. / (len(self.labels) + 1)
            w, h = dy / 2, dy / 2
            self._lines = []
            current_status = self.get_status()
            lineparams = {'color': 'k', 'linewidth': 1.25,
                          'transform': self.ax.transAxes,
                          'solid_capstyle': 'butt',
                          'animated': self._useblit}
            for i, y in enumerate(ys):
                x, y = 0.05, y - h / 2
                l1 = Line2D([x, x + w], [y + h, y], **lineparams)
                l2 = Line2D([x, x + w], [y, y + h], **lineparams)

                l1.set_visible(current_status[i])
                l2.set_visible(current_status[i])
                self._lines.append((l1, l2))
                self.ax.add_line(l1)
                self.ax.add_line(l2)
        if not hasattr(self, "_rectangles"):
            with _api.suppress_matplotlib_deprecation_warning():
                _ = self.rectangles
        return self._lines
