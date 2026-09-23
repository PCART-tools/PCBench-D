    def get_data(self):
        """Get `.StepPatch` values, edges and baseline as namedtuple."""
        StairData = namedtuple('StairData', 'values edges baseline')
        return StairData(self._values, self._edges, self._baseline)
