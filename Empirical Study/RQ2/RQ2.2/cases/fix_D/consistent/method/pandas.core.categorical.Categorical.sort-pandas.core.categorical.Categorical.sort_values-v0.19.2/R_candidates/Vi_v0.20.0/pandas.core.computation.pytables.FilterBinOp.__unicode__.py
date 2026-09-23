    def __unicode__(self):
        return pprint_thing("[Filter : [{0}] -> "
                            "[{1}]".format(self.filter[0], self.filter[1]))
