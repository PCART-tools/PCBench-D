    def locate(self, nx, ny, nx1=None, ny1=None, axes=None, renderer=None):
        # docstring inherited
        fig_w, fig_h = self._fig.bbox.size / self._fig.dpi
        x, y, w, h = self.get_position_runtime(axes, renderer)
        summed_hs = self.get_vertical_sizes(renderer)
        equal_ws = self.get_horizontal_sizes(renderer)
        y0, x0, oy, ww = _locate(
            y, x, h, w, summed_hs, equal_ws, fig_h, fig_w, self.get_anchor())
        if ny1 is None:
            _api.warn_deprecated(
                "3.5", message="Support for passing ny1=None to mean ny+1 is "
                "deprecated since %(since)s; in a future version, ny1=None "
                "will mean 'up to the last cell'.")
            ny1 = ny + 1
        x1, w1 = x0, ww
        y1, h1 = y0 + oy[ny] / fig_h, (oy[ny1] - oy[ny]) / fig_h
        return mtransforms.Bbox.from_bounds(x1, y1, w1, h1)
