    def reset_position(self):
        """
        Reset the active position to the original position.

        This undoes changes to the active position (as defined in
        `.set_position`) which may have been performed to satisfy fixed-aspect
        constraints.
        """
        for ax in self._twinned_axes.get_siblings(self):
            pos = ax.get_position(original=True)
            ax.set_position(pos, which='active')
