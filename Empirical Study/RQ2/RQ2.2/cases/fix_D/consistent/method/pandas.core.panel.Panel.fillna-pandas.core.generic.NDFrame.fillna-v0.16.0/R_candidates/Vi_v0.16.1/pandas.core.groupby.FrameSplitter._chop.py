    def _chop(self, sdata, slice_obj):
        if self.axis == 0:
            return sdata.iloc[slice_obj]
        else:
            return sdata._slice(slice_obj, axis=1)  # ix[:, slice_obj]
