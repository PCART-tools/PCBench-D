    def delete(self, loc) -> Block:
        # This will be unnecessary if/when __array_function__ is implemented
        values = self.values.delete(loc)
        mgr_locs = self._mgr_locs.delete(loc)
        return type(self)(values, placement=mgr_locs, ndim=self.ndim)
