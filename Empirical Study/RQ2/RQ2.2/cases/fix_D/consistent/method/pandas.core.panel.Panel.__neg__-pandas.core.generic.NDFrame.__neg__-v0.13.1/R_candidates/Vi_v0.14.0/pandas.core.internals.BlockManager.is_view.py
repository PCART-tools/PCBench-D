    @property
    def is_view(self):
        """ return a boolean if we are a single block and are a view """
        if len(self.blocks) == 1:
            return self.blocks[0].values.base is not None
        return False
