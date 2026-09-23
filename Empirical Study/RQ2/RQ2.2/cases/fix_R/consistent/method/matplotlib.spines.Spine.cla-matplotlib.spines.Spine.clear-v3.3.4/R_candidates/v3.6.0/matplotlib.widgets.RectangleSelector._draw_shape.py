    def _draw_shape(self, extents):
        x0, x1, y0, y1 = extents
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        xlim = sorted(self.ax.get_xlim())
        ylim = sorted(self.ax.get_ylim())

        xmin = max(xlim[0], xmin)
        ymin = max(ylim[0], ymin)
        xmax = min(xmax, xlim[1])
        ymax = min(ymax, ylim[1])

        if self._drawtype == 'box':
            self._selection_artist.set_x(xmin)
            self._selection_artist.set_y(ymin)
            self._selection_artist.set_width(xmax - xmin)
            self._selection_artist.set_height(ymax - ymin)
            self._selection_artist.set_angle(self.rotation)

        elif self._drawtype == 'line':
            self._selection_artist.set_data([xmin, xmax], [ymin, ymax])
