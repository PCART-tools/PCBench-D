    def __unicode__(self):
        """Print a generic n-ary operator and its operands using infix
        notation"""
        # recurse over the operands
        parened = ('({0})'.format(pprint_thing(opr))
                   for opr in self.operands)
        return pprint_thing(' {0} '.format(self.op).join(parened))
