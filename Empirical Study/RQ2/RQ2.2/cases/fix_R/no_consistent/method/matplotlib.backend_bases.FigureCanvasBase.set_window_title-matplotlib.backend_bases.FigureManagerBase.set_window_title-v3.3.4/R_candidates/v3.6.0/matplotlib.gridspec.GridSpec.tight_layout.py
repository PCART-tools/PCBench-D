    def tight_layout(self, figure, renderer=None,
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
            Defaults to *pad*.
        rect : tuple (left, bottom, right, top), default: None
            (left, bottom, right, top) rectangle in normalized figure
            coordinates that the whole subplots area (including labels) will
            fit into. Default (None) is the whole figure.
        """

        subplotspec_list = _tight_layout.get_subplotspec_list(
            figure.axes, grid_spec=self)
        if None in subplotspec_list:
            _api.warn_external("This figure includes Axes that are not "
                               "compatible with tight_layout, so results "
                               "might be incorrect.")

        if renderer is None:
            renderer = figure._get_renderer()

        kwargs = _tight_layout.get_tight_layout_figure(
            figure, figure.axes, subplotspec_list, renderer,
            pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)
        if kwargs:
            self.update(**kwargs)
