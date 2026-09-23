    def _make_twin_axes(self, *kl, **kwargs):
        """
        Make a twinx axes of self. This is used for twinx and twiny.
        """
        # Typically, SubplotBase._make_twin_axes is called instead of this.
        # There is also an override in axes_grid1/axes_divider.py.
        if 'sharex' in kwargs and 'sharey' in kwargs:
            raise ValueError("Twinned Axes may share only one axis.")
        ax2 = self.figure.add_axes(self.get_position(True), *kl, **kwargs)
        self.set_adjustable('datalim')
        ax2.set_adjustable('datalim')
        self._twinned_axes.join(self, ax2)
        return ax2
