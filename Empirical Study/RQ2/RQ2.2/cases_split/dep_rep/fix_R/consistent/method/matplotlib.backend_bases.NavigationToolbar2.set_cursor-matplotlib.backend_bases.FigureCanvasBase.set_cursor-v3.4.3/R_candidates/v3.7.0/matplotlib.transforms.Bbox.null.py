    @staticmethod
    def null():
        """Create a new null `Bbox` from (inf, inf) to (-inf, -inf)."""
        return Bbox([[np.inf, np.inf], [-np.inf, -np.inf]])
