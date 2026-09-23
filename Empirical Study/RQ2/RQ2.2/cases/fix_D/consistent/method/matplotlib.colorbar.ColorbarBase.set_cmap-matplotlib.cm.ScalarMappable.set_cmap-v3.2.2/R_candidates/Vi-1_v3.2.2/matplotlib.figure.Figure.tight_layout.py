    @cbook._delete_parameter("3.2", "renderer")
    def tight_layout(self, renderer=None, pad=1.08, h_pad=None, w_pad=None,
                     rect=None):
        """
        Automatically adjust subplot parameters to give specified padding.

        To exclude an artist on the axes from the bounding box calculation
        that determines the subplot parameters (i.e. legend, or annotation),
        then set `a.set_in_layout(False)` for that artist.

        Parameters
        ----------
        renderer : subclass of `~.backend_bases.RendererBase`, optional
            Defaults to the renderer for the figure.  Deprecated.
        pad : float, optional
            Padding between the figure edge and the edges of subplots,
            as a fraction of the font size.
        h_pad, w_pad : float, optional
            Padding (height/width) between edges of adjacent subplots,
            as a fraction of the font size.  Defaults to *pad*.
        rect : tuple (left, bottom, right, top), optional
            A rectangle (left, bottom, right, top) in the normalized
            figure coordinate that the whole subplots area (including
            labels) will fit into. Default is (0, 0, 1, 1).

        See Also
        --------
        .Figure.set_tight_layout
        .pyplot.tight_layout
        """

        from .tight_layout import (
            get_renderer, get_subplotspec_list, get_tight_layout_figure)
        from contextlib import suppress
        subplotspec_list = get_subplotspec_list(self.axes)
        if None in subplotspec_list:
            cbook._warn_external("This figure includes Axes that are not "
                                 "compatible with tight_layout, so results "
                                 "might be incorrect.")

        if renderer is None:
            renderer = get_renderer(self)
        ctx = (renderer._draw_disabled()
               if hasattr(renderer, '_draw_disabled')
               else suppress())
        with ctx:
            kwargs = get_tight_layout_figure(
                self, self.axes, subplotspec_list, renderer,
                pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)
        if kwargs:
            self.subplots_adjust(**kwargs)
