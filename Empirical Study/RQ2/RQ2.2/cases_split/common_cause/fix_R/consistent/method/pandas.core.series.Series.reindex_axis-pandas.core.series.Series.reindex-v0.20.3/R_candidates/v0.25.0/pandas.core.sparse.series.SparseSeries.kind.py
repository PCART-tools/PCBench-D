    @property
    def kind(self):
        if isinstance(self.sp_index, BlockIndex):
            return "block"
        elif isinstance(self.sp_index, IntIndex):
            return "integer"
