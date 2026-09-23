    def __neg__(self):
        """Negate the point."""
        coords = [-x for x in self.args]
        return Point(coords, evaluate=False)
