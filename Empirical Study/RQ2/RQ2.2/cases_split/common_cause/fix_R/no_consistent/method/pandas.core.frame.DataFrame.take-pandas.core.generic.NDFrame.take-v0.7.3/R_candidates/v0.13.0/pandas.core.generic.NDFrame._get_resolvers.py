    def _get_resolvers(self):
        d = {}
        for axis_name in self._AXIS_ORDERS:
            d.update(self._get_axis_resolvers(axis_name))
        return d
