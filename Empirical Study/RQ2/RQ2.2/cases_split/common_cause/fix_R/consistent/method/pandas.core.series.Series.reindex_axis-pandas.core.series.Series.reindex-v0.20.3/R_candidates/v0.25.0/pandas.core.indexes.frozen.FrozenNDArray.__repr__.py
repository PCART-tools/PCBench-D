    def __repr__(self):
        """
        Return a string representation for this object.
        """
        prepr = pprint_thing(self, escape_chars=("\t", "\r", "\n"), quote_strings=True)
        return "%s(%s, dtype='%s')" % (type(self).__name__, prepr, self.dtype)
