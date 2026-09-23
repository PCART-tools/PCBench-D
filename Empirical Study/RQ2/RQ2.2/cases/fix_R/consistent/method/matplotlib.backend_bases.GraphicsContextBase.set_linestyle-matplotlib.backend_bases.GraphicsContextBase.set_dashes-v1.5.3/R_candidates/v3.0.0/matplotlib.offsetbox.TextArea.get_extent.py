    def get_extent(self, renderer):
        clean_line, ismath = self._text.is_math_text(self._text._text)
        _, h_, d_ = renderer.get_text_width_height_descent(
            "lp", self._text._fontproperties, ismath=False)

        bbox, info, d = self._text._get_layout(renderer)
        w, h = bbox.width, bbox.height

        line = info[-1][0]  # last line

        self._baseline_transform.clear()

        if len(info) > 1 and self._multilinebaseline:
            d_new = 0.5 * h - 0.5 * (h_ - d_)
            self._baseline_transform.translate(0, d - d_new)
            d = d_new

        else:  # single line

            h_d = max(h_ - d_, h - d)

            if self.get_minimumdescent():
                ## to have a minimum descent, #i.e., "l" and "p" have same
                ## descents.
                d = max(d, d_)
            #else:
            #    d = d

            h = h_d + d

        return w, h, 0., d
