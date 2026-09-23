    def _print_ps(self, outfile, format, *args, **kwargs):
        papertype = kwargs.pop("papertype", rcParams['ps.papersize'])
        papertype = papertype.lower()
        if papertype == 'auto':
            pass
        elif papertype not in papersize:
            raise RuntimeError('%s is not a valid papertype. Use one of %s' %
                               (papertype, ', '.join(papersize)))

        orientation = kwargs.pop("orientation", "portrait").lower()
        if orientation == 'landscape': isLandscape = True
        elif orientation == 'portrait': isLandscape = False
        else: raise RuntimeError('Orientation must be "portrait" or "landscape"')

        self.figure.set_dpi(72) # Override the dpi kwarg
        imagedpi = kwargs.pop("dpi", 72)
        facecolor = kwargs.pop("facecolor", "w")
        edgecolor = kwargs.pop("edgecolor", "w")

        if rcParams['text.usetex']:
            self._print_figure_tex(outfile, format, imagedpi, facecolor, edgecolor,
                                   orientation, isLandscape, papertype,
                                   **kwargs)
        else:
            self._print_figure(outfile, format, imagedpi, facecolor, edgecolor,
                               orientation, isLandscape, papertype,
                               **kwargs)
