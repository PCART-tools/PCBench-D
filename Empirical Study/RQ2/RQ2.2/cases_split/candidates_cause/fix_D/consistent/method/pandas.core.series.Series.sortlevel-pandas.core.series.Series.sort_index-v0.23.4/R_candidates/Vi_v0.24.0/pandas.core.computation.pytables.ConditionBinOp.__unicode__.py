    def __unicode__(self):
        return pprint_thing("[Condition : [{cond}]]"
                            .format(cond=self.condition))
