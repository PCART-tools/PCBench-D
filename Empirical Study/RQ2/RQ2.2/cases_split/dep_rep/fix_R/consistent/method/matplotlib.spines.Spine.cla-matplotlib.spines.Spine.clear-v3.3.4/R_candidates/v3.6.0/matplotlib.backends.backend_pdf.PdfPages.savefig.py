    def savefig(self, figure=None, **kwargs):
        """
        Save a `.Figure` to this file as a new page.

        Any other keyword arguments are passed to `~.Figure.savefig`.

        Parameters
        ----------
        figure : `.Figure` or int, default: the active figure
            The figure, or index of the figure, that is saved to the file.
        """
        if not isinstance(figure, Figure):
            if figure is None:
                manager = Gcf.get_active()
            else:
                manager = Gcf.get_fig_manager(figure)
            if manager is None:
                raise ValueError("No figure {}".format(figure))
            figure = manager.canvas.figure
        # Force use of pdf backend, as PdfPages is tightly coupled with it.
        try:
            orig_canvas = figure.canvas
            figure.canvas = FigureCanvasPdf(figure)
            figure.savefig(self, format="pdf", **kwargs)
        finally:
            figure.canvas = orig_canvas
