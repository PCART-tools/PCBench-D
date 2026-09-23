    def get_bbox(self, renderer):
        _, h_, d_ = renderer.get_text_width_height_descent(
            "lp", self._text._fontproperties,
            ismath="TeX" if self._text.get_usetex() else False)

        bbox, info, yd = self._text._get_layout(renderer)
        w, h = bbox.size

        self._baseline_transform.clear()

        if len(info) > 1 and self._multilinebaseline:
            yd_new = 0.5 * h - 0.5 * (h_ - d_)
            self._baseline_transform.translate(0, yd - yd_new)
            yd = yd_new
        else:  # single line
            h_d = max(h_ - d_, h - yd)
            h = h_d + yd

        ha = self._text.get_horizontalalignment()
        x0 = {"left": 0, "center": -w / 2, "right": -w}[ha]

        return Bbox.from_bounds(x0, -yd, w, h)
