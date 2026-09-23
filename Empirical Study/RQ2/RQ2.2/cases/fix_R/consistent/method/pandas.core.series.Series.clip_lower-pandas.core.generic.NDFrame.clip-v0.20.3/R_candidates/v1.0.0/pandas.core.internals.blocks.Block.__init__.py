    def __init__(self, values, placement, ndim=None):
        self.ndim = self._check_ndim(values, ndim)
        self.mgr_locs = placement
        self.values = values

        if self._validate_ndim and self.ndim and len(self.mgr_locs) != len(self.values):
            raise ValueError(
                f"Wrong number of items passed {len(self.values)}, "
                f"placement implies {len(self.mgr_locs)}"
            )
