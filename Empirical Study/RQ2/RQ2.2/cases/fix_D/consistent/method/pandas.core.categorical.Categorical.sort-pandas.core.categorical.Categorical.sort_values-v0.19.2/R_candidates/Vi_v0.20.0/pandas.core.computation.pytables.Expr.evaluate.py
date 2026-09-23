    def evaluate(self):
        """ create and return the numexpr condition and filter """

        try:
            self.condition = self.terms.prune(ConditionBinOp)
        except AttributeError:
            raise ValueError("cannot process expression [{0}], [{1}] is not a "
                             "valid condition".format(self.expr, self))
        try:
            self.filter = self.terms.prune(FilterBinOp)
        except AttributeError:
            raise ValueError("cannot process expression [{0}], [{1}] is not a "
                             "valid filter".format(self.expr, self))

        return self.condition, self.filter
