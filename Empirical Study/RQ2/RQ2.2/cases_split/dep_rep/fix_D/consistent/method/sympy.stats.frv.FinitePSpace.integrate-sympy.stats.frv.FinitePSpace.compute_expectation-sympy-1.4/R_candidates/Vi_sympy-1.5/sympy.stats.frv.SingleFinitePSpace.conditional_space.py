    def conditional_space(self, condition):
        """
        This method is used for transferring the
        computation to probability method because
        conditional space of random variables with
        symbolic dimensions is currently not possible.
        """
        if self._is_symbolic:
            self
        domain = self.where(condition)
        prob = self.probability(condition)
        density = dict((key, val / prob)
                for key, val in self._density.items() if domain._test(key))
        return FinitePSpace(domain, density)
