    def _getitem_tuple(self, tup):

        self._has_valid_tuple(tup)
        try:
            return self._getitem_lowerdim(tup)
        except:
            pass

        retval = self.obj
        for i, key in enumerate(tup):
            if i >= self.obj.ndim:
                raise IndexingError('Too many indexers')

            if _is_null_slice(key):
                continue

            retval = getattr(retval, self.name)._getitem_axis(key, axis=i)

        return retval
