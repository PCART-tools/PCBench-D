    @property
    def is_view(self):
        """ return a boolean if I am possibly a view """
        return self.values.base is not None
