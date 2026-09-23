    def _getitem_tuple(self, tup):
        try:
            return self._getitem_lowerdim(tup)
        except IndexingError:
            pass

        # no multi-index, so validate all of the indexers
        self._has_valid_tuple(tup)

        # ugly hack for GH #836
        if self._multi_take_opportunity(tup):
            return self._multi_take(tup)

        # no shortcut needed
        retval = self.obj
        for i, key in enumerate(tup):
            if com.is_null_slice(key):
                continue

            retval = getattr(retval, self.name)._getitem_axis(key, axis=i)

        return retval
