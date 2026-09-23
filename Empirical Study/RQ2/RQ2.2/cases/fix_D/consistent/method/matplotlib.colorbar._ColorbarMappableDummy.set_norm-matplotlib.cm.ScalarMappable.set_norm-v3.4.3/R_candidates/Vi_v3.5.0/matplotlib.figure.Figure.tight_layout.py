    def tight_layout(self, *, pad=1.08, h_pad=None, w_pad=None, rect=None):
        """
        Adjust the padding between and around subplots.

        To exclude an artist on the Axes from the bounding box calculation
        that determines the subplot parameters (i.e. legend, or annotation),
        set ``a.set_in_layout(False)`` for that artist.

        Parameters
        ----------
        pad : float, default: 1.08
            Padding between the figure edge and the edges of subplots,
            as a fraction of the font size.
        h_pad, w_pad : float, default: *pad*
            Padding (height/width) between edges of adjacent subplots,
            as a fraction of the font size.
        rect : tuple (left, bottom, right, top), default: (0, 0, 1, 1)
            A rectangle in normalized figure coordinates into which the whole
            subplots area (including labels) will fit.

        See Also
        --------
        .Figure.set_tight_layout
        .pyplot.tight_layout
        """
        from contextlib import nullcontext
        from .tight_layout import (
            get_subplotspec_list, get_tight_layout_figure)
        subplotspec_list = get_subplotspec_list(self.axes)
        if None in subplotspec_list:
            _api.warn_external("This figure includes Axes that are not "
                               "compatible with tight_layout, so results "
                               "might be incorrect.")
        renderer = _get_renderer(self)
        with getattr(renderer, "_draw_disabled", nullcontext)():
            kwargs = get_tight_layout_figure(
                self, self.axes, subplotspec_list, renderer,
                pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)
        if kwargs:
            self.subplots_adjust(**kwargs)
