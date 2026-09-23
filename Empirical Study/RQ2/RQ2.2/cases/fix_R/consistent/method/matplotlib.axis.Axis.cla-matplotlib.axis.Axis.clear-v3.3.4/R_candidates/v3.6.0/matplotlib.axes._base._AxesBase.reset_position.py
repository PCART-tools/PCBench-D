    def reset_position(self):
        """
        Reset the active position to the original position.

        This resets the possible position change due to aspect constraints.
        For an explanation of the positions see `.set_position`.
        """
        for ax in self._twinned_axes.get_siblings(self):
            pos = ax.get_position(original=True)
            ax.set_position(pos, which='active')
