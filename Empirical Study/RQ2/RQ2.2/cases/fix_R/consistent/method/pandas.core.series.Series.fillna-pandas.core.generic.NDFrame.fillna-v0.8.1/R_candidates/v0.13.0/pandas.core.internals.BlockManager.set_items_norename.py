    def set_items_norename(self, value):
        self.set_axis(0, value, maybe_rename=False, check_axis=False)
        self._shape = None
