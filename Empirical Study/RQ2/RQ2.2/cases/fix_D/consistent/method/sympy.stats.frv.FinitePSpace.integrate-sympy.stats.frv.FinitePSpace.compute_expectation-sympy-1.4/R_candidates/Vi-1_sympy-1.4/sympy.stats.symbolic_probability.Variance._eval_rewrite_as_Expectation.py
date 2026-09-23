    def _eval_rewrite_as_Expectation(self, arg, condition=None, **kwargs):
            e1 = Expectation(arg**2, condition)
            e2 = Expectation(arg, condition)**2
            return e1 - e2
