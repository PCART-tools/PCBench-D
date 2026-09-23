    def _eval_rewrite_as_Integral(self, arg, condition=None, **kwargs):
        return probability(arg, condition, evaluate=False)
