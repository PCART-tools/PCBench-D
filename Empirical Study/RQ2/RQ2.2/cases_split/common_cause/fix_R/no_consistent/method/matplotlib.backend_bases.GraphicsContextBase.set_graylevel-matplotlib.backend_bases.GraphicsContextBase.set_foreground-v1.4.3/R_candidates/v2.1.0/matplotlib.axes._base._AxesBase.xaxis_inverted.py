    def xaxis_inverted(self):
        """Returns *True* if the x-axis is inverted."""
        left, right = self.get_xlim()
        return right < left
