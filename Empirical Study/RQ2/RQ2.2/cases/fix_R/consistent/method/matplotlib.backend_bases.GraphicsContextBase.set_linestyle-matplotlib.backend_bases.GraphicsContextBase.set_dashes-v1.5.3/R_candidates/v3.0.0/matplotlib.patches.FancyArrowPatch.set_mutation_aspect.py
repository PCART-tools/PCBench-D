    def set_mutation_aspect(self, aspect):
        """
        Set the aspect ratio of the bbox mutation.

        Parameters
        ----------
        aspect : scalar
        """
        self._mutation_aspect = aspect
        self.stale = True
