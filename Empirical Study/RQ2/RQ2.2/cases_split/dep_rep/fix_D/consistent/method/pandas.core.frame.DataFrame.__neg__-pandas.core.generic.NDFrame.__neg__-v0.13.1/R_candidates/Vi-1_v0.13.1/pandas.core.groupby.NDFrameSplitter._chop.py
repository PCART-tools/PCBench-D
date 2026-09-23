    def _chop(self, sdata, slice_obj):
        return self.factory(sdata.get_slice(slice_obj, axis=self.axis))
