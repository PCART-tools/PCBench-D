    @property
    def density(self):
        r = float(self.sp_index.npoints) / float(self.sp_index.length)
        return r
