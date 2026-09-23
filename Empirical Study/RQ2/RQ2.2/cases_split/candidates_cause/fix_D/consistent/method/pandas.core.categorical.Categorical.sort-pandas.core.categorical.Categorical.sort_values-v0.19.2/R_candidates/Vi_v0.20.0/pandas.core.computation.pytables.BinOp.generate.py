    def generate(self, v):
        """ create and return the op string for this TermValue """
        val = v.tostring(self.encoding)
        return "(%s %s %s)" % (self.lhs, self.op, val)
