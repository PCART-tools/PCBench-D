    def yaxis_inverted(self):
        """Returns *True* if the y-axis is inverted."""
        bottom, top = self.get_ylim()
        return top < bottom
