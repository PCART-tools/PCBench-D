    @property
    def _is_symbolic(self):
        """
        Helper property to check if the distribution
        of the random variable is having symbolic
        dimension.
        """
        return self.distribution.is_symbolic
