    def tight_layout(self, renderer=None, pad=1.08, h_pad=None, w_pad=None,
                     rect=None):
        """
        Adjust subplot parameters to give specified padding.

        Parameters:

          pad : float
            padding between the figure edge and the edges of subplots,
            as a fraction of the font-size.
          h_pad, w_pad : float
            padding (height/width) between edges of adjacent subplots.
            Defaults to `pad_inches`.
          rect : if rect is given, it is interpreted as a rectangle
            (left, bottom, right, top) in the normalized figure
            coordinate that the whole subplots area (including
            labels) will fit into. Default is (0, 0, 1, 1).
        """

        from .tight_layout import (
            get_renderer, get_subplotspec_list, get_tight_layout_figure)

        subplotspec_list = get_subplotspec_list(self.axes)
        if None in subplotspec_list:
            warnings.warn("This figure includes Axes that are not compatible "
                          "with tight_layout, so results might be incorrect.")

        if renderer is None:
            renderer = get_renderer(self)

        kwargs = get_tight_layout_figure(
            self, self.axes, subplotspec_list, renderer,
            pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)
        self.subplots_adjust(**kwargs)
