    def _print_ps(self, outfile, format, *args,
                  papertype=None, dpi=72, facecolor='w', edgecolor='w',
                  orientation='portrait',
                  **kwargs):
        if papertype is None:
            papertype = rcParams['ps.papersize']
        papertype = papertype.lower()
        cbook._check_in_list(['auto', *papersize], papertype=papertype)

        orientation = cbook._check_getitem(
            _Orientation, orientation=orientation.lower())

        self.figure.set_dpi(72)  # Override the dpi kwarg

        printer = (self._print_figure_tex
                   if rcParams['text.usetex'] else
                   self._print_figure)
        printer(outfile, format, dpi, facecolor, edgecolor,
                orientation, papertype, **kwargs)
