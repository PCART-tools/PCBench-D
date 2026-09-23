    def execute_constrained_layout(self, renderer=None):
        """
        Use ``layoutgrid`` to determine pos positions within Axes.

        See also `.set_constrained_layout_pads`.
        """

        from matplotlib._constrained_layout import do_constrained_layout
        from matplotlib.tight_layout import get_renderer

        _log.debug('Executing constrainedlayout')
        if self._layoutgrid is None:
            _api.warn_external("Calling figure.constrained_layout, but "
                               "figure not setup to do constrained layout. "
                               "You either called GridSpec without the "
                               "figure keyword, you are using plt.subplot, "
                               "or you need to call figure or subplots "
                               "with the constrained_layout=True kwarg.")
            return
        w_pad, h_pad, wspace, hspace = self.get_constrained_layout_pads()
        # convert to unit-relative lengths
        fig = self
        width, height = fig.get_size_inches()
        w_pad = w_pad / width
        h_pad = h_pad / height
        if renderer is None:
            renderer = get_renderer(fig)
        do_constrained_layout(fig, renderer, h_pad, w_pad, hspace, wspace)
