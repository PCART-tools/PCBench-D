    def _wrap_agged_manager(self, mgr: Manager) -> Series:
        return self.obj._constructor(mgr, name=self.obj.name)
