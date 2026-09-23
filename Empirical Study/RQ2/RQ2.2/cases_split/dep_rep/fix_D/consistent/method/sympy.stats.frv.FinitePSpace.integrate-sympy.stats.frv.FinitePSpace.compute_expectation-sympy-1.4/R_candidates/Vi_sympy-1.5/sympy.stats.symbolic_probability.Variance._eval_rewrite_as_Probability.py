    def _eval_rewrite_as_Probability(self, arg, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Probability)
