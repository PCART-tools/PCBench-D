    def _eval_rewrite_as_Integral(self, arg, condition=None, **kwargs):
        return expectation(arg, condition=condition, evaluate=False)
