    def __str__(self) -> str:
        return pprint_thing(self, quote_strings=True, escape_chars=("\t", "\r", "\n"))
