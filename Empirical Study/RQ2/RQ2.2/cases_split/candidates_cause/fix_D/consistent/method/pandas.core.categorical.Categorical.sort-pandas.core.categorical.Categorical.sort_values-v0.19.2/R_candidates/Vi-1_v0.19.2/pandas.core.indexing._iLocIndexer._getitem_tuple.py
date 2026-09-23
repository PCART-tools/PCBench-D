    def _getitem_tuple(self, tup):

        self._has_valid_tuple(tup)
        try:
            return self._getitem_lowerdim(tup)
        except:
            pass

        retval = self.obj
        axis = 0
        for i, key in enumerate(tup):
            if i >= self.obj.ndim:
                raise IndexingError('Too many indexers')

            if is_null_slice(key):
                axis += 1
                continue

            retval = getattr(retval, self.name)._getitem_axis(key, axis=axis)

            # if the dim was reduced, then pass a lower-dim the next time
            if retval.ndim < self.ndim:
                axis -= 1

            # try to get for the next axis
            axis += 1

        return retval
