    def __str__(self):
        operands = map(str, self.operands)
        return pprint_thing("{0}({1})".format(self.op, ",".join(operands)))
