    def __unicode__(self):
        """
        Return a string representation for this object.

        Invoked by unicode(df) in py2 only. Yields a Unicode String in both
        py2/py3.
        """
        prepr = com.pprint_thing(self, escape_chars=('\t', '\r', '\n'),
                                 quote_strings=True)
        return "%s(%s, dtype='%s')" % (type(self).__name__, prepr, self.dtype)
