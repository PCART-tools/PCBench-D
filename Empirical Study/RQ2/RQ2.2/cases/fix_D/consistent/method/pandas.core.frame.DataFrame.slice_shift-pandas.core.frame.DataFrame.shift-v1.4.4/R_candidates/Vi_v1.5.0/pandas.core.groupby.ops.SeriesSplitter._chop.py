    def _chop(self, sdata: Series, slice_obj: slice) -> Series:
        # fastpath equivalent to `sdata.iloc[slice_obj]`
        mgr = sdata._mgr.get_slice(slice_obj)
        ser = sdata._constructor(mgr, name=sdata.name, fastpath=True)
        return ser.__finalize__(sdata, method="groupby")
