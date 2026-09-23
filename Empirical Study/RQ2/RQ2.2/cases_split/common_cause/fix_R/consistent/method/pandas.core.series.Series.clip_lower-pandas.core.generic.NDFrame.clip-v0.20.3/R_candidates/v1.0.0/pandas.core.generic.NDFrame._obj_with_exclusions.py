    @property
    def _obj_with_exclusions(self: FrameOrSeries) -> FrameOrSeries:
        """ internal compat with SelectionMixin """
        return self
