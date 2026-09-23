    def _get_val_at(self, loc):
        n = len(self)
        if loc < 0:
            loc += n

        if loc >= n or loc < 0:
            raise IndexError("Out of bounds access")

        sp_loc = self.sp_index.lookup(loc)
        if sp_loc == -1:
            return self.fill_value
        else:
            return libindex.get_value_at(self.sp_values, sp_loc)
