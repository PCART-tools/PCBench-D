    def set_mutation_scale(self, scale):
        """
        Set the mutation scale.

        ACCEPTS: float
        """
        self._mutation_scale = scale
        self.stale = True
