    def generate(self, v):
        """ create and return the op string for this TermValue """
        val = v.tostring(self.encoding)
        return "({lhs} {op} {val})".format(lhs=self.lhs, op=self.op, val=val)
