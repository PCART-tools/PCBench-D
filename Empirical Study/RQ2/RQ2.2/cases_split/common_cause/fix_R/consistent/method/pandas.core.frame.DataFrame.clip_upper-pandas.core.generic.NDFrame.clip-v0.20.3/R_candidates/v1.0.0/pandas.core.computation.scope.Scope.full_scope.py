    @property
    def full_scope(self):
        """
        Return the full scope for use with passing to engines transparently
        as a mapping.

        Returns
        -------
        vars : DeepChainMap
            All variables in this scope.
        """
        maps = [self.temps] + self.resolvers.maps + self.scope.maps
        return DeepChainMap(*maps)
