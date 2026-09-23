    def _eval_rewrite_as_Sum(self, arg, condition=None, **kwargs):
        return probability(arg, condition, evaluate=False)
