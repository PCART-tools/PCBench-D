    def __unicode__(self):

        # don't want to print out all of the items here
        name = pprint_thing(self.__class__.__name__)
        if self._is_single_block:

            result = '%s: %s dtype: %s' % (name, len(self), self.dtype)

        else:

            shape = ' x '.join([pprint_thing(s) for s in self.shape])
            result = '%s: %s, %s, dtype: %s' % (name, pprint_thing(
                self.mgr_locs.indexer), shape, self.dtype)

        return result
