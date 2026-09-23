    def __unicode__(self):

        # don't want to print out all of the items here
        name = pprint_thing(self.__class__.__name__)
        if self._is_single_block:

            result = '{name}: {len} dtype: {dtype}'.format(
                name=name, len=len(self), dtype=self.dtype)

        else:

            shape = ' x '.join(pprint_thing(s) for s in self.shape)
            result = '{name}: {index}, {shape}, dtype: {dtype}'.format(
                name=name, index=pprint_thing(self.mgr_locs.indexer),
                shape=shape, dtype=self.dtype)

        return result
