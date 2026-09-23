    def locate(self, nx, ny, nx1=None, ny1=None, axes=None, renderer=None):
        # docstring inherited
        fig_w, fig_h = self._fig.bbox.size / self._fig.dpi
        x, y, w, h = self.get_position_runtime(axes, renderer)
        summed_ws = self.get_horizontal_sizes(renderer)
        equal_hs = self.get_vertical_sizes(renderer)
        x0, y0, ox, hh = _locate(
            x, y, w, h, summed_ws, equal_hs, fig_w, fig_h, self.get_anchor())
        if nx1 is None:
            _api.warn_deprecated(
                "3.5", message="Support for passing nx1=None to mean nx+1 is "
                "deprecated since %(since)s; in a future version, nx1=None "
                "will mean 'up to the last cell'.")
            nx1 = nx + 1
        x1, w1 = x0 + ox[nx] / fig_w, (ox[nx1] - ox[nx]) / fig_w
        y1, h1 = y0, hh
        return mtransforms.Bbox.from_bounds(x1, y1, w1, h1)
