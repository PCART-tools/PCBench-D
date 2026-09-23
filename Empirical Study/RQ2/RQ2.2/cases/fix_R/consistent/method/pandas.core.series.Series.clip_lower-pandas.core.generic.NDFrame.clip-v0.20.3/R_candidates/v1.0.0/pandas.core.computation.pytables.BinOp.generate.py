    def generate(self, v) -> str:
        """ create and return the op string for this TermValue """
        val = v.tostring(self.encoding)
        return f"({self.lhs} {self.op} {val})"
