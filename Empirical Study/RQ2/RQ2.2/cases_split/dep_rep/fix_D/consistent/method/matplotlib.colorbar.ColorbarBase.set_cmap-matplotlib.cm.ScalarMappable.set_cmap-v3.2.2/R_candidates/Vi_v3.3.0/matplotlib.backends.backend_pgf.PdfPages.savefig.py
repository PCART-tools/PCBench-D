    def savefig(self, figure=None, **kwargs):
        """
        Save a `.Figure` to this file as a new page.

        Any other keyword arguments are passed to `~.Figure.savefig`.

        Parameters
        ----------
        figure : `.Figure` or int, optional
            Specifies what figure is saved to file. If not specified, the
            active figure is saved. If a `.Figure` instance is provided, this
            figure is saved. If an int is specified, the figure instance to
            save is looked up by number.
        """
        if not isinstance(figure, Figure):
            if figure is None:
                manager = Gcf.get_active()
            else:
                manager = Gcf.get_fig_manager(figure)
            if manager is None:
                raise ValueError("No figure {}".format(figure))
            figure = manager.canvas.figure

        try:
            orig_canvas = figure.canvas
            figure.canvas = FigureCanvasPgf(figure)

            width, height = figure.get_size_inches()
            if self._n_figures == 0:
                self._write_header(width, height)
            else:
                # \pdfpagewidth and \pdfpageheight exist on pdftex, xetex, and
                # luatex<0.85; they were renamed to \pagewidth and \pageheight
                # on luatex>=0.85.
                self._file.write(
                    br'\newpage'
                    br'\ifdefined\pdfpagewidth\pdfpagewidth'
                    br'\else\pagewidth\fi=%ain'
                    br'\ifdefined\pdfpageheight\pdfpageheight'
                    br'\else\pageheight\fi=%ain'
                    b'%%\n' % (width, height)
                )

            figure.savefig(self._file, format="pgf", **kwargs)
            self._n_figures += 1
        finally:
            figure.canvas = orig_canvas
