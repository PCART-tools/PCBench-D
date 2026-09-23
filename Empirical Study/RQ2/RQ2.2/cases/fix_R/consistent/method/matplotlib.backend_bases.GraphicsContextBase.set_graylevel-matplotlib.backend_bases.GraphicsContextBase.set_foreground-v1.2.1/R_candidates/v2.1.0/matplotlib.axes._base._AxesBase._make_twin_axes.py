    def _make_twin_axes(self, *kl, **kwargs):
        """
        make a twinx axes of self. This is used for twinx and twiny.
        """
        ax2 = self.figure.add_axes(self.get_position(True), *kl, **kwargs)
        return ax2
