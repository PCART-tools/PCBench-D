    def _make_twin_axes(self, *args, **kwargs):
        """Make a twinx axes of self. This is used for twinx and twiny."""
        # Typically, SubplotBase._make_twin_axes is called instead of this.
        if 'sharex' in kwargs and 'sharey' in kwargs:
            raise ValueError("Twinned Axes may share only one axis")
        ax2 = self.figure.add_axes(
            self.get_position(True), *args, **kwargs,
            axes_locator=_TransformedBoundsLocator(
                [0, 0, 1, 1], self.transAxes))
        self.set_adjustable('datalim')
        ax2.set_adjustable('datalim')
        self._twinned_axes.join(self, ax2)
        return ax2
