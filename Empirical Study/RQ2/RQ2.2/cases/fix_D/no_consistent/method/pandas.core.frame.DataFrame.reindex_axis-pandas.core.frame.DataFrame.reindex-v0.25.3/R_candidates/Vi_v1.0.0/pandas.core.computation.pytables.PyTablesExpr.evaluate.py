    def evaluate(self):
        """ create and return the numexpr condition and filter """

        try:
            self.condition = self.terms.prune(ConditionBinOp)
        except AttributeError:
            raise ValueError(
                f"cannot process expression [{self.expr}], [{self}] "
                "is not a valid condition"
            )
        try:
            self.filter = self.terms.prune(FilterBinOp)
        except AttributeError:
            raise ValueError(
                f"cannot process expression [{self.expr}], [{self}] "
                "is not a valid filter"
            )

        return self.condition, self.filter
