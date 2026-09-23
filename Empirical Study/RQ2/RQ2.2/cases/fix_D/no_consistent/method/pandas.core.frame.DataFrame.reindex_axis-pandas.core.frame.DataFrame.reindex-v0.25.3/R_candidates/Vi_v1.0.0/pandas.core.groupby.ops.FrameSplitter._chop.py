    def _chop(self, sdata: DataFrame, slice_obj: slice) -> DataFrame:
        if self.axis == 0:
            return sdata.iloc[slice_obj]
        else:
            return sdata._slice(slice_obj, axis=1)
