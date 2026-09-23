    def compute_expectation(self, expr, condition=None, evaluate=True, **kwargs):
        """
        Transfers the task of handling queries to the specific stochastic
        process because every process has their own logic of handling such
        queries.
        """
        return self.process.expectation(expr, condition, evaluate, **kwargs)
