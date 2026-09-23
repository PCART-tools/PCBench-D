    @property
    def nlevels(self) -> int:
        if self.index:
            return getattr(self.data_index, "nlevels", 1)
        else:
            return 0
