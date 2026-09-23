    def execute(self, fig):
        """
        Execute tight_layout.

        This decides the subplot parameters given the padding that
        will allow the axes labels to not be covered by other labels
        and axes.

        Parameters
        ----------
        fig : `.Figure` to perform layout on.

        See also: `.figure.Figure.tight_layout` and `.pyplot.tight_layout`.
        """
        info = self._params
        subplotspec_list = get_subplotspec_list(fig.axes)
        if None in subplotspec_list:
            _api.warn_external("This figure includes Axes that are not "
                               "compatible with tight_layout, so results "
                               "might be incorrect.")
        renderer = fig._get_renderer()
        with getattr(renderer, "_draw_disabled", nullcontext)():
            kwargs = get_tight_layout_figure(
                fig, fig.axes, subplotspec_list, renderer,
                pad=info['pad'], h_pad=info['h_pad'], w_pad=info['w_pad'],
                rect=info['rect'])
        if kwargs:
            fig.subplots_adjust(**kwargs)
