    def evaluate(self):
        """ create and return the numexpr condition and filter """

        try:
            self.condition = self.terms.prune(ConditionBinOp)
        except AttributeError:
            raise ValueError("cannot process expression [{expr}], [{slf}] "
                             "is not a valid condition".format(expr=self.expr,
                                                               slf=self))
        try:
            self.filter = self.terms.prune(FilterBinOp)
        except AttributeError:
            raise ValueError("cannot process expression [{expr}], [{slf}] "
                             "is not a valid filter".format(expr=self.expr,
                                                            slf=self))

        return self.condition, self.filter
