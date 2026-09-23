    @final
    def copy(self, deep: bool = True):
        """copy constructor"""
        values = self.values
        if deep:
            values = values.copy()
        return type(self)(values, placement=self._mgr_locs, ndim=self.ndim)
