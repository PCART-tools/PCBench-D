    def __unicode__(self):
        from pandas.core.common import pprint_thing
        return pprint_thing(self, quote_strings=True,
                            escape_chars=('\t', '\r', '\n'))
