    @staticmethod
    def unit():
        """Create a new unit `Bbox` from (0, 0) to (1, 1)."""
        return Bbox(np.array([[0.0, 0.0], [1.0, 1.0]], float))
