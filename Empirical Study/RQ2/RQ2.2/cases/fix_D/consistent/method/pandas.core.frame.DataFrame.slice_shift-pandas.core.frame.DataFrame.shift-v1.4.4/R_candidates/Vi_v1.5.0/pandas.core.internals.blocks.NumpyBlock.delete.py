    def delete(self, loc) -> Block:
        values = np.delete(self.values, loc, 0)
        mgr_locs = self._mgr_locs.delete(loc)
        return type(self)(values, placement=mgr_locs, ndim=self.ndim)
