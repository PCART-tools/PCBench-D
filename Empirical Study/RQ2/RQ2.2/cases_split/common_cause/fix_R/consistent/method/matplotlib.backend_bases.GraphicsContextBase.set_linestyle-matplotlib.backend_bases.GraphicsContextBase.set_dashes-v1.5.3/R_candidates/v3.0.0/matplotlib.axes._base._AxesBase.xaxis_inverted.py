    def xaxis_inverted(self):
        """Return whether the x-axis is inverted."""
        left, right = self.get_xlim()
        return right < left
