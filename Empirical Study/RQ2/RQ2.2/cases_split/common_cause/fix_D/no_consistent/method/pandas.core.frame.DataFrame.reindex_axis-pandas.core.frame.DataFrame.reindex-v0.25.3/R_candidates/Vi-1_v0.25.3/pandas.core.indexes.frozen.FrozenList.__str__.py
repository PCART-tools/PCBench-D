    def __str__(self):
        return pprint_thing(self, quote_strings=True, escape_chars=("\t", "\r", "\n"))
