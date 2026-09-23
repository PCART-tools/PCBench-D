    def register(self, *projections):
        """
        Register a new set of projections.
        """
        for projection in projections:
            name = projection.name
            self._all_projection_types[name] = projection
