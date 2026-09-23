    def __unicode__(self):
        if self.subtype is None:
            return "interval"
        return "interval[{subtype}]".format(subtype=self.subtype)
