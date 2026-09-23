    def evaluate(self):
        self.condition = "(%s %s %s)" % (
            self.lhs.condition,
            self.op,
            self.rhs.condition)
        return self
