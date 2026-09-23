    def _eval_rewrite_as_Integral(self, arg1, arg2, condition=None, **kwargs):
        return covariance(self.args[0], self.args[1], self._condition, evaluate=False)
