    def _wrap_agged_manager(self, mgr: Manager2D) -> DataFrame:
        return self.obj._constructor(mgr)
