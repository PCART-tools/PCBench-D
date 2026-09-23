    @final
    def delete(self, loc) -> list[Block]:
        # This will be unnecessary if/when __array_function__ is implemented
        if self.ndim == 1:
            values = self.values.delete(loc)
            mgr_locs = self._mgr_locs.delete(loc)
            return [type(self)(values, placement=mgr_locs, ndim=self.ndim)]
        elif self.values.ndim == 1:
            # We get here through to_stata
            return []
        return super().delete(loc)
