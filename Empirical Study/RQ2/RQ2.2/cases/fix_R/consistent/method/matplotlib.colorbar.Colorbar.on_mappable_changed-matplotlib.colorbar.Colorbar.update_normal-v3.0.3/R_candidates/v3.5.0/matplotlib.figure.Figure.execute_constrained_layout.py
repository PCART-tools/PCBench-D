    def execute_constrained_layout(self, renderer=None):
        """
        Use ``layoutgrid`` to determine pos positions within Axes.

        See also `.set_constrained_layout_pads`.

        Returns
        -------
        layoutgrid : private debugging object
        """

        from matplotlib._constrained_layout import do_constrained_layout

        _log.debug('Executing constrainedlayout')
        w_pad, h_pad, wspace, hspace = self.get_constrained_layout_pads()
        # convert to unit-relative lengths
        fig = self
        width, height = fig.get_size_inches()
        w_pad = w_pad / width
        h_pad = h_pad / height
        if renderer is None:
            renderer = _get_renderer(fig)
        return do_constrained_layout(fig, renderer, h_pad, w_pad,
                                     hspace, wspace)
