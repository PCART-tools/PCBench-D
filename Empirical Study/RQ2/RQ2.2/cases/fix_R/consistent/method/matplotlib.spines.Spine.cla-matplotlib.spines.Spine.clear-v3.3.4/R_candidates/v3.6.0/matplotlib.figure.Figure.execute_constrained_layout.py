    @_api.deprecated("3.6", alternative="figure.get_layout_engine().execute()")
    def execute_constrained_layout(self, renderer=None):
        """
        Use ``layoutgrid`` to determine pos positions within Axes.

        See also `.set_constrained_layout_pads`.

        Returns
        -------
        layoutgrid : private debugging object
        """
        if not isinstance(self.get_layout_engine(), ConstrainedLayoutEngine):
            return None
        return self.get_layout_engine().execute(self)
