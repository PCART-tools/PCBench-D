    @property
    def density(self):
        """
        Ratio of non-sparse points to total (dense) data points
        represented in the frame
        """
        tot_nonsparse = sum(ser.sp_index.npoints
                            for _, ser in compat.iteritems(self))
        tot = len(self.index) * len(self.columns)
        return tot_nonsparse / float(tot)
