    def __unicode__(self):
        contents = '\n'.join(repr(c) for c in self._chunks)
        return '{self}\n{contents}'.format(self=object.__repr__(self),
                                           contents=pprint_thing(contents))
