    def evaluate(self):
        self.condition = "({lhs} {op} {rhs})".format(lhs=self.lhs.condition,
                                                     op=self.op,
                                                     rhs=self.rhs.condition)
        return self
