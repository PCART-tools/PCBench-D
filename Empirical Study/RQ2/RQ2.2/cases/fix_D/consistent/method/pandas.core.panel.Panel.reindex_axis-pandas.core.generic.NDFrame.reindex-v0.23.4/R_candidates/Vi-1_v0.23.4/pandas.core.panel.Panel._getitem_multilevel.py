    def _getitem_multilevel(self, key):
        info = self._info_axis
        loc = info.get_loc(key)
        if isinstance(loc, (slice, np.ndarray)):
            new_index = info[loc]
            result_index = maybe_droplevels(new_index, key)
            slices = [loc] + [slice(None) for x in range(self._AXIS_LEN - 1)]
            new_values = self.values[slices]

            d = self._construct_axes_dict(self._AXIS_ORDERS[1:])
            d[self._info_axis_name] = result_index
            result = self._constructor(new_values, **d)
            return result
        else:
            return self._get_item_cache(key)
