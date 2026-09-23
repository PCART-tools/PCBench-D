    def point_at_t(self, t):
        """Evaluate curve at a single point *t*. Returns a Tuple[float*d]."""
        return tuple(self(t))
