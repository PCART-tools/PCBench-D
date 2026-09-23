    def _get_shared_axes(self):
        """Return Grouper of shared axes for current axis."""
        return self.axes._shared_axes[
            self._get_axis_name()].get_siblings(self.axes)
