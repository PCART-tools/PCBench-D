    def get_text_width_height_descent(self, tex, fontsize, renderer=None):
        """
        return width, heigth and descent of the text.
        """
        if tex.strip() == '':
            return 0, 0, 0

        if renderer:
            dpi_fraction = renderer.points_to_pixels(1.)
        else:
            dpi_fraction = 1.

        if rcParams['text.latex.preview']:
            # use preview.sty
            basefile = self.get_basefile(tex, fontsize)
            baselinefile = '%s.baseline' % basefile

            if DEBUG or not os.path.exists(baselinefile):
                dvifile = self.make_dvi_preview(tex, fontsize)

            with open(baselinefile) as fh:
                l = fh.read().split()
            height, depth, width = [float(l1) * dpi_fraction for l1 in l]
            return width, height + depth, depth

        else:
            # use dviread. It sometimes returns a wrong descent.
            dvifile = self.make_dvi(tex, fontsize)
            with dviread.Dvi(dvifile, 72 * dpi_fraction) as dvi:
                page = next(iter(dvi))
            # A total height (including the descent) needs to be returned.
            return page.width, page.height + page.descent, page.descent
