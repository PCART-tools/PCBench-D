    def _eval_rewrite_as_Expectation(self, arg1, arg2, condition=None, **kwargs):
        e1 = Expectation(arg1*arg2, condition)
        e2 = Expectation(arg1, condition)*Expectation(arg2, condition)
        return e1 - e2
