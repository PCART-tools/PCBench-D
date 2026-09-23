    def __unicode__(self):
        return pprint_thing('{0}({1})'.format(self.op, self.operand))
