    @property
    def axes(self):
        "index(es) of the NDFrame"
        # we do it this way because if we have reversed axes, then
        # the block manager shows then reversed
        return [self._get_axis(a) for a in self._AXIS_ORDERS]
