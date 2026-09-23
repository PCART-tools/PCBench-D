    @property
    def shape(self):
        if self.ndim == 1:
            return ((len(self.values)),)
        return (len(self.mgr_locs), len(self.values))
