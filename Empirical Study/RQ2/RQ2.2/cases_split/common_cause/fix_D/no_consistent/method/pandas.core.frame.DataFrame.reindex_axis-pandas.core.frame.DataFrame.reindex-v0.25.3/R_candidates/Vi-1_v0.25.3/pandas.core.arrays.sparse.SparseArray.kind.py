    @property
    def kind(self):
        """
        The kind of sparse index for this array. One of {'integer', 'block'}.
        """
        if isinstance(self.sp_index, IntIndex):
            return "integer"
        else:
            return "block"
