    def _print_ps(self, outfile, format, *args,
                  papertype=None, dpi=72, facecolor='w', edgecolor='w',
                  orientation='portrait',
                  **kwargs):
        if papertype is None:
            papertype = rcParams['ps.papersize']
        papertype = papertype.lower()
        if papertype == 'auto':
            pass
        elif papertype not in papersize:
            raise RuntimeError('%s is not a valid papertype. Use one of %s' %
                               (papertype, ', '.join(papersize)))

        orientation = orientation.lower()
        cbook._check_in_list(['landscape', 'portrait'],
                             orientation=orientation)
        isLandscape = (orientation == 'landscape')

        self.figure.set_dpi(72)  # Override the dpi kwarg

        if rcParams['text.usetex']:
            self._print_figure_tex(outfile, format, dpi, facecolor, edgecolor,
                                   orientation, isLandscape, papertype,
                                   **kwargs)
        else:
            self._print_figure(outfile, format, dpi, facecolor, edgecolor,
                               orientation, isLandscape, papertype,
                               **kwargs)
