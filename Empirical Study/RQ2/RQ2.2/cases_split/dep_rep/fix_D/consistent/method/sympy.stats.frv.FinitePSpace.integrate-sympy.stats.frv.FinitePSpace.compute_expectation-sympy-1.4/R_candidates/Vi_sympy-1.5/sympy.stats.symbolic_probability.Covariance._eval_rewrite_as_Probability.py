    def _eval_rewrite_as_Probability(self, arg1, arg2, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Probability)
