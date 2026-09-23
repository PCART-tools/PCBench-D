    def _eval_rewrite_as_Integral(self, arg, condition=None, **kwargs):
        return variance(self.args[0], self._condition, evaluate=False)
