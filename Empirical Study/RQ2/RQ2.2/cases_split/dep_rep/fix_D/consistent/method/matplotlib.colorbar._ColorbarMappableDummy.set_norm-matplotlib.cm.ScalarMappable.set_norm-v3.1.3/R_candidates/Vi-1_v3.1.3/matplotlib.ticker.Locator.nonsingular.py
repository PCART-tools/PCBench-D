    def nonsingular(self, v0, v1):
        """Expand a range as needed to avoid singularities."""
        return mtransforms.nonsingular(v0, v1, expander=.05)
