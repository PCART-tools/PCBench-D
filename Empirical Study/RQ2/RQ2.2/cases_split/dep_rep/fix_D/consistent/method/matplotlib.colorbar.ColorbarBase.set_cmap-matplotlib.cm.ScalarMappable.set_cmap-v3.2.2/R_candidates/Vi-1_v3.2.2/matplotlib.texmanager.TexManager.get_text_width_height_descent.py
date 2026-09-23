    def get_text_width_height_descent(self, tex, fontsize, renderer=None):
        """Return width, height and descent of the text."""
        if tex.strip() == '':
            return 0, 0, 0

        dpi_fraction = renderer.points_to_pixels(1.) if renderer else 1

        if rcParams['text.latex.preview']:
            # use preview.sty
            basefile = self.get_basefile(tex, fontsize)
            baselinefile = '%s.baseline' % basefile

            if not os.path.exists(baselinefile):
                dvifile = self.make_dvi_preview(tex, fontsize)

            with open(baselinefile) as fh:
                l = fh.read().split()
            height, depth, width = [float(l1) * dpi_fraction for l1 in l]
            return width, height + depth, depth

        else:
            # use dviread.
            dvifile = self.make_dvi(tex, fontsize)
            with dviread.Dvi(dvifile, 72 * dpi_fraction) as dvi:
                page, = dvi
            # A total height (including the descent) needs to be returned.
            return page.width, page.height + page.descent, page.descent
