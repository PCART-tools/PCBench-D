    def tight_layout(self, fig, renderer=None,
                     pad=1.08, h_pad=None, w_pad=None, rect=None):
        """
        Adjust subplot parameters to give specified padding.

        Parameters
        ----------

        pad : float
            Padding between the figure edge and the edges of subplots, as a
            fraction of the font-size.
        h_pad, w_pad : float, optional
            Padding (height/width) between edges of adjacent subplots.
            Defaults to ``pad_inches``.
        rect : tuple of 4 floats, optional
            (left, bottom, right, top) rectangle in normalized figure
            coordinates that the whole subplots area (including labels) will
            fit into.  Default is (0, 0, 1, 1).
        """

        from .tight_layout import (
            get_renderer, get_subplotspec_list, get_tight_layout_figure)

        subplotspec_list = get_subplotspec_list(fig.axes, grid_spec=self)
        if None in subplotspec_list:
            warnings.warn("This figure includes Axes that are not compatible "
                          "with tight_layout, so results might be incorrect.")

        if renderer is None:
            renderer = get_renderer(fig)

        kwargs = get_tight_layout_figure(
            fig, fig.axes, subplotspec_list, renderer,
            pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)
        self.update(**kwargs)
