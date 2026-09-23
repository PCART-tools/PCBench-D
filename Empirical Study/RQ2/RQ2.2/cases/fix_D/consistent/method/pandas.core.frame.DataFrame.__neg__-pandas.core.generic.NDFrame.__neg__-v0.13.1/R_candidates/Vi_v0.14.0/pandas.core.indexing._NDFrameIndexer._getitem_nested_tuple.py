    def _getitem_nested_tuple(self, tup):
        # we have a nested tuple so have at least 1 multi-index level
        # we should be able to match up the dimensionaility here

        # we have too many indexers for our dim, but have at least 1
        # multi-index dimension, try to see if we have something like
        # a tuple passed to a series with a multi-index
        if len(tup) > self.ndim:
            result = self._handle_lowerdim_multi_index_axis0(tup)
            if result is not None:
                return result

            # this is a series with a multi-index specified a tuple of selectors
            return self._getitem_axis(tup, axis=0, validate_iterable=True)

        # handle the multi-axis by taking sections and reducing
        # this is iterative
        obj = self.obj
        axis = 0
        for key in tup:

            if _is_null_slice(key):
                axis += 1
                continue

            current_ndim = obj.ndim
            obj = getattr(obj, self.name)._getitem_axis(key, axis=axis, validate_iterable=True)
            axis += 1

            # if we have a scalar, we are done
            if np.isscalar(obj):
                break

            # has the dim of the obj changed?
            # GH 7199
            if obj.ndim < current_ndim:
                axis -= 1

        return obj
