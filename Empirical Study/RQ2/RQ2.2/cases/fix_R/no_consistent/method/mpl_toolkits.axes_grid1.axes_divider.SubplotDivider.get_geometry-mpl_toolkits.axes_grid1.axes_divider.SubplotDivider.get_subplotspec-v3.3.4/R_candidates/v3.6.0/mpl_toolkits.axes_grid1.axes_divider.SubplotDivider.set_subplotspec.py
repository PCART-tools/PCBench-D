    def set_subplotspec(self, subplotspec):
        """Set the SubplotSpec instance."""
        self._subplotspec = subplotspec
        self.set_position(subplotspec.get_position(self.figure))
