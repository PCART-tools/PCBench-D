    def _getitem_tuple(self, tup: Tuple):

        self._has_valid_tuple(tup)
        try:
            return self._getitem_lowerdim(tup)
        except IndexingError:
            pass

        retval = self.obj
        axis = 0
        for i, key in enumerate(tup):
            if com.is_null_slice(key):
                axis += 1
                continue

            retval = getattr(retval, self.name)._getitem_axis(key, axis=axis)

            # if the dim was reduced, then pass a lower-dim the next time
            if retval.ndim < self.ndim:
                # TODO: this is never reached in tests; can we confirm that
                #  it is impossible?
                axis -= 1

            # try to get for the next axis
            axis += 1

        return retval
