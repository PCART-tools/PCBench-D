    def __array_wrap__(self, result, context=None):
        result = lib.item_from_zerodim(result)
        if is_scalar(result):
            # e.g. we get here with np.ptp(series)
            # ptp also requires the item_from_zerodim
            return result
        d = self._construct_axes_dict(self._AXIS_ORDERS, copy=False)
        return self._constructor(result, **d).__finalize__(self)
