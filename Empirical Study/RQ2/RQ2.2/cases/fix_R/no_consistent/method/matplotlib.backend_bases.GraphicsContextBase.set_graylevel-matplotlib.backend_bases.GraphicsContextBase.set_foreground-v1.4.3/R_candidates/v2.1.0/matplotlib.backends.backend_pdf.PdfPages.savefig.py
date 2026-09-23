    def savefig(self, figure=None, **kwargs):
        """
        Saves a :class:`~matplotlib.figure.Figure` to this file as a new page.

        Any other keyword arguments are passed to
        :meth:`~matplotlib.figure.Figure.savefig`.

        Parameters
        ----------

        figure : :class:`~matplotlib.figure.Figure` or int, optional
            Specifies what figure is saved to file. If not specified, the
            active figure is saved. If a :class:`~matplotlib.figure.Figure`
            instance is provided, this figure is saved. If an int is specified,
            the figure instance to save is looked up by number.
        """
        if isinstance(figure, Figure):
            figure.savefig(self, format='pdf', **kwargs)
        else:
            if figure is None:
                figureManager = Gcf.get_active()
            else:
                figureManager = Gcf.get_fig_manager(figure)
            if figureManager is None:
                raise ValueError("No such figure: " + repr(figure))
            else:
                figureManager.canvas.figure.savefig(self, format='pdf',
                                                    **kwargs)
