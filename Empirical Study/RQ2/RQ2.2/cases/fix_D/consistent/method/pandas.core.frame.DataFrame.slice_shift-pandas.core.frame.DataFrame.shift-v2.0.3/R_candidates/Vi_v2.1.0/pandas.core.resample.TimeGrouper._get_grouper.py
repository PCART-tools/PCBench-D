    def _get_grouper(
        self, obj: NDFrameT, validate: bool = True
    ) -> tuple[BinGrouper, NDFrameT]:
        # create the resampler and return our binner
        r = self._get_resampler(obj)
        return r.grouper, cast(NDFrameT, r.obj)
