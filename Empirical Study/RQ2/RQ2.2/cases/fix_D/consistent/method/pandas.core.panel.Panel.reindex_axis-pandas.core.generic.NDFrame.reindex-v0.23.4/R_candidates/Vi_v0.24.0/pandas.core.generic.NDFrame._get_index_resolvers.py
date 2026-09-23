    def _get_index_resolvers(self):
        d = {}
        for axis_name in self._AXIS_ORDERS:
            d.update(self._get_axis_resolvers(axis_name))
        return d
