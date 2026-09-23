    def get_position(self):
        """Return the bounds of the subplot box."""
        return self.get_subplotspec().get_position(self.figure).bounds
