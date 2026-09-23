    @_api.deprecated("3.7",
                     addendum="Any custom property styling may be lost.")
    @property
    def rectangles(self):
        if not hasattr(self, "_rectangles"):
            ys = np.linspace(1, 0, len(self.labels)+2)[1:-1]
            dy = 1. / (len(self.labels) + 1)
            w, h = dy / 2, dy / 2
            rectangles = self._rectangles = [
                Rectangle(xy=(0.05, ys[i] - h / 2), width=w, height=h,
                          edgecolor="black",
                          facecolor="none",
                          transform=self.ax.transAxes
                          )
                for i, y in enumerate(ys)
            ]
            self._frames.set_visible(False)
            for rectangle in rectangles:
                self.ax.add_patch(rectangle)
        if not hasattr(self, "_lines"):
            with _api.suppress_matplotlib_deprecation_warning():
                _ = self.lines
        return self._rectangles
