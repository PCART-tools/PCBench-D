    def probability(self, condition):
        if self._is_symbolic:
            #TODO: Implement the mechanism for handling queries for symbolic sized distributions.
            raise NotImplementedError("Currently, probability queries are not "
            "supported for random variables with symbolic sized distributions.")
        condition = rv_subs(condition)
        return FinitePSpace(self.domain, self.distribution).probability(condition)
