    def evaluate(self):
        self.condition = f"({self.lhs.condition} {self.op} {self.rhs.condition})"
        return self
