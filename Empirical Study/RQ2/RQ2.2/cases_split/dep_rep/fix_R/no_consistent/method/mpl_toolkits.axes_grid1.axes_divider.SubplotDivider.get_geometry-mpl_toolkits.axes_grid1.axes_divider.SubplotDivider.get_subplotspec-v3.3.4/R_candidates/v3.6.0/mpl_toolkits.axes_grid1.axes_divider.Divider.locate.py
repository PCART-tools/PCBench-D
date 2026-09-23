    def locate(self, nx, ny, nx1=None, ny1=None, axes=None, renderer=None):
        """
        Parameters
        ----------
        nx, nx1 : int
            Integers specifying the column-position of the
            cell. When *nx1* is None, a single *nx*-th column is
            specified. Otherwise location of columns spanning between *nx*
            to *nx1* (but excluding *nx1*-th column) is specified.
        ny, ny1 : int
            Same as *nx* and *nx1*, but for row positions.
        axes
        renderer
        """

        fig_w, fig_h = self._fig.bbox.size / self._fig.dpi
        x, y, w, h = self.get_position_runtime(axes, renderer)

        hsizes = self.get_horizontal_sizes(renderer)
        vsizes = self.get_vertical_sizes(renderer)
        k_h = self._calc_k(hsizes, fig_w * w)
        k_v = self._calc_k(vsizes, fig_h * h)

        if self.get_aspect():
            k = min(k_h, k_v)
            ox = self._calc_offsets(hsizes, k)
            oy = self._calc_offsets(vsizes, k)

            ww = (ox[-1] - ox[0]) / fig_w
            hh = (oy[-1] - oy[0]) / fig_h
            pb = mtransforms.Bbox.from_bounds(x, y, w, h)
            pb1 = mtransforms.Bbox.from_bounds(x, y, ww, hh)
            x0, y0 = pb1.anchored(self.get_anchor(), pb).p0

        else:
            ox = self._calc_offsets(hsizes, k_h)
            oy = self._calc_offsets(vsizes, k_v)
            x0, y0 = x, y

        if nx1 is None:
            _api.warn_deprecated(
                "3.5", message="Support for passing nx1=None to mean nx+1 is "
                "deprecated since %(since)s; in a future version, nx1=None "
                "will mean 'up to the last cell'.")
            nx1 = nx + 1
        if ny1 is None:
            _api.warn_deprecated(
                "3.5", message="Support for passing ny1=None to mean ny+1 is "
                "deprecated since %(since)s; in a future version, ny1=None "
                "will mean 'up to the last cell'.")
            ny1 = ny + 1

        x1, w1 = x0 + ox[nx] / fig_w, (ox[nx1] - ox[nx]) / fig_w
        y1, h1 = y0 + oy[ny] / fig_h, (oy[ny1] - oy[ny]) / fig_h

        return mtransforms.Bbox.from_bounds(x1, y1, w1, h1)
