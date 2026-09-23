    def __unicode__(self):
        return '%s\nFill: %s\n%s' % (printing.pprint_thing(self),
                                     printing.pprint_thing(self.fill_value),
                                     printing.pprint_thing(self.sp_index))
