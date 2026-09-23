    def set_subplotspec(self, subplotspec):
        """Set the `.SubplotSpec`. associated with the subplot."""
        self._subplotspec = subplotspec
        self._set_position(subplotspec.get_position(self.get_figure(root=False)))
