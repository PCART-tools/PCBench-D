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

            # this is a series with a multi-index specified a tuple of
            # selectors
            return self._getitem_axis(tup, axis=self.axis)

        # handle the multi-axis by taking sections and reducing
        # this is iterative
        obj = self.obj
        axis = 0
        for i, key in enumerate(tup):

            if com.is_null_slice(key):
                axis += 1
                continue

            current_ndim = obj.ndim
            obj = getattr(obj, self.name)._getitem_axis(key, axis=axis)
            axis += 1

            # if we have a scalar, we are done
            if is_scalar(obj) or not hasattr(obj, 'ndim'):
                break

            # has the dim of the obj changed?
            # GH 7199
            if obj.ndim < current_ndim:

                # GH 7516
                # if had a 3 dim and are going to a 2d
                # axes are reversed on a DataFrame
                if i >= 1 and current_ndim == 3 and obj.ndim == 2:
                    obj = obj.T

                axis -= 1

        return obj
