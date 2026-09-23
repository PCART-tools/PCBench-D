    def __unicode__(self):
        # format the tz
        return "datetime64[{unit}, {tz}]".format(unit=self.unit, tz=self.tz)
