    def _indexed_same(self, other):
        return all([self._get_axis(a).equals(other._get_axis(a))
                    for a in self._AXIS_ORDERS])
