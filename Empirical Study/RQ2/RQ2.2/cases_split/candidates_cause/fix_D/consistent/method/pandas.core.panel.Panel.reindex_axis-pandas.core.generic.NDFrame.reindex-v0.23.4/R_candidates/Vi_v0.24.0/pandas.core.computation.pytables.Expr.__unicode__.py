    def __unicode__(self):
        if self.terms is not None:
            return pprint_thing(self.terms)
        return pprint_thing(self.expr)
