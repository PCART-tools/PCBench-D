    def _chop(self, sdata: Series, slice_obj: slice) -> Series:
        return sdata._get_values(slice_obj)
