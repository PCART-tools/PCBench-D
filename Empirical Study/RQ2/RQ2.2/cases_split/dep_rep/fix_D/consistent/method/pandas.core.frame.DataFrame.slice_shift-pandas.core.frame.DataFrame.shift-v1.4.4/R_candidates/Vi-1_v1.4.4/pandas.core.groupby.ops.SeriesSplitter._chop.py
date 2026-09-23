    def _chop(self, sdata: Series, slice_obj: slice) -> Series:
        # fastpath equivalent to `sdata.iloc[slice_obj]`
        mgr = sdata._mgr.get_slice(slice_obj)
        # __finalize__ not called here, must be applied by caller if applicable
        return sdata._constructor(mgr, name=sdata.name, fastpath=True)
