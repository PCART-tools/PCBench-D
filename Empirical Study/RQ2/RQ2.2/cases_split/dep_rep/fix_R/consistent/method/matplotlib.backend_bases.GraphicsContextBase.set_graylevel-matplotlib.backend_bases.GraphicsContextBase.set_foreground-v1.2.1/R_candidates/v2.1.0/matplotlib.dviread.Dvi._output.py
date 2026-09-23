    def _output(self):
        """
        Output the text and boxes belonging to the most recent page.
        page = dvi._output()
        """
        minx, miny, maxx, maxy = np.inf, np.inf, -np.inf, -np.inf
        maxy_pure = -np.inf
        for elt in self.text + self.boxes:
            if isinstance(elt, Box):
                x, y, h, w = elt
                e = 0           # zero depth
            else:               # glyph
                x, y, font, g, w = elt
                h, e = font._height_depth_of(g)
            minx = min(minx, x)
            miny = min(miny, y - h)
            maxx = max(maxx, x + w)
            maxy = max(maxy, y + e)
            maxy_pure = max(maxy_pure, y)

        if self.dpi is None:
            # special case for ease of debugging: output raw dvi coordinates
            return Page(text=self.text, boxes=self.boxes,
                        width=maxx-minx, height=maxy_pure-miny,
                        descent=maxy-maxy_pure)

        # convert from TeX's "scaled points" to dpi units
        d = self.dpi / (72.27 * 2**16)
        if self.baseline is None:
            descent = (maxy - maxy_pure) * d
        else:
            descent = self.baseline

        text = [Text((x-minx)*d, (maxy-y)*d - descent, f, g, w*d)
                for (x, y, f, g, w) in self.text]
        boxes = [Box((x-minx)*d, (maxy-y)*d - descent, h*d, w*d)
                 for (x, y, h, w) in self.boxes]

        return Page(text=text, boxes=boxes, width=(maxx-minx)*d,
                    height=(maxy_pure-miny)*d, descent=descent)
