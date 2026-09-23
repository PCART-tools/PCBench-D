    def register(self, *projections):
        """
        Register a new set of projection(s).
        """
        for projection in projections:
            name = projection.name
            self._all_projection_types[name] = projection
