    @property
    def _holder(self):
        # For extension blocks, the holder is values-dependent.
        return type(self.values)
