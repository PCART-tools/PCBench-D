    def parse(self):
        """Parse an expression"""
        return self._visitor.visit(self.expr)
