    def __unicode__(self):
        return pprint_thing("[Filter : [{lhs}] -> [{op}]"
                            .format(lhs=self.filter[0], op=self.filter[1]))
