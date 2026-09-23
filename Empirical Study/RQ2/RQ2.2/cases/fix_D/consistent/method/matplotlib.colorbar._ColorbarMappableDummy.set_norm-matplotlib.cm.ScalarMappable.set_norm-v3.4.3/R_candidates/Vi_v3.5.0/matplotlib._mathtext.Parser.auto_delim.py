    def auto_delim(self, s, loc, toks):
        front, middle, back = toks

        return self._auto_sized_delimiter(front, middle.asList(), back)
