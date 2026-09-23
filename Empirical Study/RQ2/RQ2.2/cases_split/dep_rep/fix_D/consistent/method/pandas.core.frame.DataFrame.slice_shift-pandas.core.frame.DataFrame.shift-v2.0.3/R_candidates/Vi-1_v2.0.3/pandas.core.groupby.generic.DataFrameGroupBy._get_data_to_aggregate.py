    def _get_data_to_aggregate(
        self, *, numeric_only: bool = False, name: str | None = None
    ) -> Manager2D:
        obj = self._obj_with_exclusions
        if self.axis == 1:
            mgr = obj.T._mgr
        else:
            mgr = obj._mgr

        if numeric_only:
            mgr = mgr.get_numeric_data(copy=False)
        return mgr
