    def set_mutation_scale(self, scale):
        """
        Set the mutation scale.

        Parameters
        ----------
        scale : scalar
        """
        self._mutation_scale = scale
        self.stale = True
