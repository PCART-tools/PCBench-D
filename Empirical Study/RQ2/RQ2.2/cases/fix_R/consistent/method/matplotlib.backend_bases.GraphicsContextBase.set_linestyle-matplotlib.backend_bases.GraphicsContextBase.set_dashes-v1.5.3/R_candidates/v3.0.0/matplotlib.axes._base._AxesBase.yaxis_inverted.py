    def yaxis_inverted(self):
        """Return whether the y-axis is inverted."""
        bottom, top = self.get_ylim()
        return top < bottom
