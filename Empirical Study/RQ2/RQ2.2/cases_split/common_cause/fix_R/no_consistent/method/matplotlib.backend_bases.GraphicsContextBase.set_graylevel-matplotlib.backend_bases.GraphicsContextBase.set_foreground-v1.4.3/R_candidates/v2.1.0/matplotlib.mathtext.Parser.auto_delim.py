    def auto_delim(self, s, loc, toks):
        #~ print "auto_delim", toks
        front, middle, back = toks

        return self._auto_sized_delimiter(front, middle.asList(), back)
