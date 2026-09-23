    def __unicode__(self):
        contents = '\n'.join(repr(c) for c in self._chunks)
        return '%s\n%s' % (object.__repr__(self), pprint_thing(contents))
