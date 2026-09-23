    def __unicode__(self):
        return '{self}\nFill: {fill}\n{index}'.format(
            self=printing.pprint_thing(self),
            fill=printing.pprint_thing(self.fill_value),
            index=printing.pprint_thing(self.sp_index))
