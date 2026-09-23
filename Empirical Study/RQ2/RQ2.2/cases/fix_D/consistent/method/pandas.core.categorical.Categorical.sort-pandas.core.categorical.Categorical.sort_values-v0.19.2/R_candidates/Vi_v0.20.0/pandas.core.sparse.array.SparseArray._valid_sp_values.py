    @property
    def _valid_sp_values(self):
        sp_vals = self.sp_values
        mask = notnull(sp_vals)
        return sp_vals[mask]
