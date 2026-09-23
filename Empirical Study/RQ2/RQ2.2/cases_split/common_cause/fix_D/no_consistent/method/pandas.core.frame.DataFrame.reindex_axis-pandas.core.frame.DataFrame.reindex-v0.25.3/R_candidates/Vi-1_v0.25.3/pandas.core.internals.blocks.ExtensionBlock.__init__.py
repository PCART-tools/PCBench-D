    def __init__(self, values, placement, ndim=None):
        values = self._maybe_coerce_values(values)
        super().__init__(values, placement, ndim)
